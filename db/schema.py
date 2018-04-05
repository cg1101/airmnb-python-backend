
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

metadata = sa.MetaData()


##########################################################################


t_users = sa.Table('users', metadata,
	sa.Column('id', pg.UUID, primary_key=True, autoincrement=False, key=u'userId', doc=''),
	sa.Column('family_name', pg.TEXT, nullable=False, key=u'familyName', doc=''),
	sa.Column('given_name', pg.TEXT, nullable=False, key=u'givenName', doc=''),
	sa.Column('gender', pg.TEXT, key=u'gender', doc=''),
	sa.Column('dob', pg.DATE, nullable=False, unique=True, key=u'dob', doc=''),
	sa.Column('email', pg.TEXT, nullable=False, unique=True, key=u'email', doc=''),
	sa.Column('source_type', pg.TEXT, nullable=False, unique=True, key=u'sourceType', doc=''),
	sa.Column('avartar', pg.BYTEA, nullable=False, unique=True, key=u'avartar', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, unique=True, key=u'createdAt', doc=''),
)


##########################################################################


__all__ = [name for name in locals().keys()
		if name.startswith('t_') or name.startswith('j_')]
__all__.insert(0, 'metadata')
