#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application import application as app
from db import database as db

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def list(detailed=False):
	for rule in app.url_map.iter_rules():
		print('{0} methods: {1} -> {2}'.format(str(rule), ','.join(rule.methods), rule.endpoint))

if __name__ == '__main__':
	manager.run()
