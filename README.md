# airmnb-python-backend


## Setup Development Environment

### Prerequisites

Please make sure following prerequisites are all installed.

 - python
 - pip
 - PostgreSQL server
 - psql

### install virtualenv

Please follow the instructions in https://virtualenv.pypa.io/en/stable/installation/ to install virtualenv first.

### clone code repo and install dependencies

```
$ git clone https://github.com/cg1101/airmnb-python-backend

$ cd airmnb-python-backend

$ virtualenv venv

$ . venv/bin/activate

$ pip install -r requirements.txt
```

### setup database

#### create database

Plese use following command to create database
```
createdb airmmb
```

#### setup db uri

Edit setenv.sh, set the ```DATABASE_URI``` to following value

```
export DATABASE_URI=postgresql://localhost/airmnb
```

A more general pattern will be:
```
export DATABASE_URI=postgresql://username:password@hostname:port/database_name
```

After you have updated setenv.sh, load it into current environment:
```
source setenv.sh
```

Then you can verify it by running:
```
psql ${DATABASE_URI}
```
This should open psql and connect to the database you created. Then enter ```\q``` to quit.


#### initialize database for database migration

If you just created database, it hasn't been initialized yet. Run following command:

```
python manage.py db downgrade base
```

This step is only needed for the first time after installation. It will create a table in public schema called 'alembic_version'. If 
you have run this before, then you shouldn't run this command again, otherwise the existing data will be wiped out.

#### run database migration script

You may upgrade the db schema to the latest version by running:
```
python manage.py db upgrade head
```

### add convenience commands

For your convenience, you can add following command to your .bash_profile to quickly jump to your working folder.

```
alias <myalias>='cd <my_po>; . venv/bin/activate; . setenv.sh'
```

