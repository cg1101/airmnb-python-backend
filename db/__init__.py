
import sys

from flask_sqlalchemy import SQLAlchemy

from .schema import metadata

mode = 'app' if 'app' in sys.modules else 'shell'

database = SQLAlchemy(metadata=metadata)
