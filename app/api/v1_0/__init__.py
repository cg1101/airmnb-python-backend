#!/usr/bin/env python

import os
import glob
import importlib

from flask import Blueprint, jsonify

from .. import InvalidUsage


api_1_0 = Blueprint('api_1_0', __name__)


@api_1_0.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response


for i in glob.glob(os.path.join(os.path.dirname(__file__), '*.py')):
	mod_name = '.' + os.path.basename(i).split('.')[0]
	importlib.import_module(mod_name, 'app.api.v1_0')
