#!/usr/bin/env python

# import cStringIO
import traceback
from functools import wraps

from flask import Response, request, make_response, jsonify, current_app, session, g
from werkzeug.exceptions import HTTPException
from werkzeug.datastructures import CombinedMultiDict, FileStorage

from app.i18n import get_text as _
from db.db import SS


class InvalidUsage(Exception):
	status_code = 400

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload
	def to_dict(self):
		rv = dict(self.payload or ())
		rv['error'] = self.message
		return rv


def api(fn):
	@wraps(fn)
	def decorated(*args, **kwargs):
		'''
		api handlers generally return responses with mimetype set to json,
		this can be changed by returning a response instead (e.g. froma file
		download handler).
		'''
		try:
			result = fn(*args, **kwargs)
			if isinstance(result, dict):
				resp = jsonify(result)
			elif isinstance(result, Response):
				resp = result
			else:
				raise RuntimeError('unexpected datatype returned from api handler')
		except InvalidUsage as e:
			resp = make_response(jsonify(e.to_dict()), e.status_code, {})
			SS.rollback()
		except HTTPException as e:
			#
			# Normally we should not end up being here because all api
			# handlers are suppose to raise InvalidUsage and such Exceptions
			# should be caught by api version blueprint's error handler.
			# In case there are non-compliant handlers that are still using
			# using HTTPException directly, we explicitly convert it to a
			# JSON response.
			#
			resp = make_response(jsonify({'error': '%s' % e}), e.code, {})
			SS.rollback()
		except Exception as e:
			#
			# Oops! Caught unhandled exception, log what happend
			# and return an error response to client
			#
			# out = cStringIO.StringIO()
			# traceback.print_exc(file=out)
			# current_app.logger.error('\033[1;31mERROR caught inside api:\033[0m\n%s\n' % out.getvalue())

			# TODO: hide debug information for production deployment
			resp = make_response((jsonify({'error': '%s' % e}), 500, {}))
			SS.rollback()
		else:
			SS.commit()
		return resp
	return decorated


def caps(*caps):
	def customized_decorator(fn):
		@wraps(fn)
		def decorated(*args, **kwargs):
			user = g.current_user
			missing = set(caps) - set(getattr(user, 'caps', set()))
			if missing:
				raise InvalidUsage(
					_('not enough capabilities to perform requested operation'),
					403,
					{'missing': list(missing)}
				)
			return fn(*args, **kwargs)
		return decorated
	return customized_decorator


class validators:
	@classmethod
	def is_mandatory(cls, data, key, value):
		if key not in data:
			raise ValueError(_('mandatory parameter missing'))
	@classmethod
	def non_blank(cls, data, key, value):
		if not isinstance(value, basestring) or not value.strip():
			raise ValueError(_('must be non-blank string'))
	@classmethod
	def enum(cls, data, key, value, *options):
		if value not in options:
			raise ValueError(_('must be one of {0}').format(
					','.join(options)))
	@classmethod
	def is_number(cls, data, key, value, max_value=None, min_value=None,
			le=None, lt=None, gt=None, ge=None):
		if max_value is not None and value > max_value:
			raise ValueError(_('value {0} must not be greater than {1}'
				).format(value, max_value))
		if min_value is not None and value < min_value:
			raise ValueError(_('value {0} must not be less than {1}'
				).format(value, min_value))
		if le and not value <= le:
			raise ValueError(_('value {0} must be less than or equal to {1}'
				).format(value, le))
		if lt and not value < lt:
			raise ValueError(_('value {0} must be less than {1}'
				).format(value, lt))
		if ge and not value >= ge:
			raise ValueError(_('value {0} must be greater than or equal to {1}'
				).format(value, ge))
		if gt and not value > gt:
			raise ValueError(_('value {0} must be greater than {1}'
				).format(value, gt))
	@classmethod
	def is_string(cls, data, key, value, length=None, max_length=None,
			min_length=None):
		if value is not None:
			if not isinstance(value, basestring):
				raise ValueError(_('value must of a string'))
			if length is not None and len(value) != length:
				raise ValueError(_('value length must be {0}'
					).format(length))
			if max_length is not None and len(value) > max_length:
				raise ValueError(_('value length must not be longer than {0}'
					).format(max_length))
			if min_length is not None and len(value) < min_length:
				raise ValueError(_('value length must not be shorter than {0}'
					).format(min_length))
	@classmethod
	def not_null(cls, data, key, value):
		if value is None:
			raise ValueError(_('value must not be None'))
	@classmethod
	def is_bool(cls, data, key, value):
		if value is not None:
			if not (value is True or value is False):
				# expression:
				# value not in (False, True)
				# won't work because 1 == True is always True
				raise ValueError(_('value must be a boolean'))
	@classmethod
	def is_file(cls, data, key, value):
		if value is not None:
			if not isinstance(value, FileStorage):
				raise ValueError(_('value must be of type FileStorage'))

	# @classmethod
	# def is_list(cls, data, key, value):
	# 	if value is not None:
	# 		if not isinstance(value, list):
	# 			raise ValueError('value must be a list')



class Field(object):
	def __init__(self, name, is_mandatory=False, default=None,
			normalizer=None, validators=[]):
		self.name = name
		self.is_mandatory = is_mandatory
		self.default = default
		self.normalizer = normalizer
		self.validators = []
		for x in validators:
			args = ()
			kwargs = {}
			if isinstance(x, tuple):
				if len(x) == 1:
					func = x[0]
				elif len(x) == 2:
					func, args = x
				elif len(x) == 3:
					func, args, kwargs = x
				else:
					raise ValueError('invalid validator specification %s' % x)
			else:
				func = x
			if not callable(func) or not isinstance(args, tuple) or not isinstance(kwargs, dict):
				raise ValueError('invalid validator specification: %s' % x)
			self.validators.append((func, args, kwargs))

	def validate(self, data, output):
		key = self.name
		# print '\033[1;32m'
		# print '=' * 80
		# print '\033[0;36m'
		# print 'validating', key
		# print '\033[1;34m'
		# print '-' * 80
		# print '\033[0m'
		if key in data:
			value = data[key]
		else:
			if self.default is not None:
				value = self.default() if callable(self.default) else self.default
			else:
				if self.is_mandatory:
					raise InvalidUsage(_('{0}: mandatory parameter missing').format(key))
				# non-mandatory parameter is omitted, skip further validation
				return
		try:
			if self.normalizer:
				#
				# use output as context, this makes it possible
				# to pass in extra parameters to normalizers
				# either as view_args, or mandatory parameters
				#
				value = self.normalizer(output, key, value)
				#
				#value = self.normalizer(data, key, value)
				#
			for func, args, kwargs in self.validators:
				#
				# Note:
				# To make context-aware validators work properly,
				# we use normalized output as context, as below:
				#
				func(output, key, value, *args, **kwargs)
				#
				# instead of following:
				#
				# func(data, key, value, *args, **kwargs)
				#
				# This is because validators of later fields
				# may need to work on normalized values
				#
		except ValueError as exc:
			raise InvalidUsage(_('{0}: {1}').format(key, exc))
		except Exception as exc:
			# out = cStringIO.StringIO()
			# traceback.print_exc(file=out)
			# error = out.getvalue()
			# current_app.logger.error('\033[1;31mERROR caught inside validate():\033[0m\n%s\n' % error)
			raise
			raise RuntimeError(_('{0}: {1}').format(key, exc))
		output[key] = value
		return


class MyForm(object):
	def __init__(self, *fields):
		self.field_names = []
		self.field_by_name = {}
		for i in fields:
			self.add_field(i)

	def add_field(self, field):
		if not isinstance(field, Field):
			raise TypeError('field must be instance of class Field')
		if field.name in self.field_by_name:
			raise ValueError('a field named \'%s\' already exists' % field.name)
		self.field_names.append(field.name)
		self.field_by_name[field.name] = field

	def get_data(self, with_view_args=True, is_json=True, copy=False, use_args=False):
		if is_json:
			try:
				data = request.get_json() or {}
				if use_args:
					data.update(request.args)
			except Exception as exc:
				raise InvalidUsage(_('error decoding json from incoming request'))
		else:
			data = request.values
		data = CombinedMultiDict([data, request.files])
		output = {}
		if copy:
			# for some reason, following statement doesn't work
			# output.update(data)
			# so we have to use following statement
			for k in data.keys():
				output[k] = data[k]
		if with_view_args:
			output.update(request.view_args)
		for key in self.field_names:
			f = self.field_by_name[key]
			f.validate(data, output)
		return output


from .v1_0 import api_1_0
