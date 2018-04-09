
import sys

from flask_sqlalchemy import SQLAlchemy

from .schema import metadata

mode = 'app' if sys.modules.has_key('app') else 'shell'

database = SQLAlchemy(metadata=metadata)
