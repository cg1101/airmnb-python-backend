
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

metadata = sa.MetaData()


##########################################################################


t_users = sa.Table('users', metadata,
	sa.Column('id', pg.UUID, primary_key=True, autoincrement=False, key=u'userId', doc=''),
	sa.Column('family_name', pg.TEXT, nullable=False, key=u'familyName', doc=''),
	sa.Column('given_name', pg.TEXT, nullable=False, key=u'givenName', doc=''),
	sa.Column('gender', pg.TEXT, key=u'gender', doc=''),
	sa.Column('dob', pg.DATE, nullable=False, key=u'dob', doc=''),
	sa.Column('email', pg.TEXT, nullable=False, key=u'email', doc=''),
	sa.Column('source_type', pg.TEXT, key=u'sourceType', doc=''),
	sa.Column('avartar', pg.BYTEA, key=u'avartar', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
)


t_babies = sa.Table('babies', metadata,
	sa.Column('id', pg.UUID, primary_key=True, autoincrement=False, key=u'babyId', doc=''),
	sa.Column('family_name', pg.TEXT, nullable=False, key=u'familyName', doc=''),
	sa.Column('given_name', pg.TEXT, nullable=False, key=u'givenName', doc=''),
	sa.Column('gender', pg.TEXT, key=u'gender', doc=''),
	sa.Column('dob', pg.DATE, nullable=False, key=u'dob', doc=''),
	sa.Column('parent_id', pg.UUID, nullable=False, key=u'parentId', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, key=u'createdAt', doc=''),
	sa.ForeignKeyConstraint([u'parentId'], [u'users.userId']),
)


t_locations = sa.Table('locations', metadata,
	sa.Column('id', pg.UUID, primary_key=True, autoincrement=True, key=u'locationId', doc=''),
	sa.Column('langitude', pg.DOUBLE_PRECISION, nullable=False, key=u'langitude', doc=''),
	sa.Column('latitude', pg.DOUBLE_PRECISION, nullable=False, key=u'latitude', doc=''),
	sa.Column('addr1', pg.TEXT, nullable=False, key=u'addr1', doc=''),
	sa.Column('addr2', pg.TEXT, key=u'addr2', doc=''),
	sa.Column('addr3', pg.TEXT, key=u'addr3', doc=''),
	sa.Column('city', pg.TEXT, nullable=False, key=u'city', doc=''),
	sa.Column('state', pg.TEXT, nullable=False, key=u'state', doc=''),
	sa.Column('country', pg.TEXT, nullable=False, key=u'country', doc=''),
	sa.Column('postcode', pg.TEXT, key=u'postcode', doc=''),
)


t_activities = sa.Table('activities', metadata,
	sa.Column('id', pg.UUID, primary_key=True, autoincrement=False, key=u'activityId', doc=''),
	sa.Column('name', pg.TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('description', pg.TEXT, key=u'description', doc=''),
	sa.Column('location_id', pg.UUID, nullable=False, key=u'locationId', doc=''),
	sa.ForeignKeyConstraint([u'locationId'], [u'locations.locationId']),
)


##########################################################################


__all__ = [name for name in locals().keys()
		if name.startswith('t_') or name.startswith('j_')]
__all__.insert(0, 'metadata')
