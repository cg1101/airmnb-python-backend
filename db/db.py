
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import config
from . import database, mode

if mode == 'app':
	SS = database.session
else:
	engine = create_engine(config['development'].SQLALCHEMY_DATABASE_URI)
	SS = scoped_session(sessionmaker(bind=engine))

__all__ = ['SS']
