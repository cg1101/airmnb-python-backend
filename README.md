# airmnb-python-backend


## Setup Development Environment

### Prerequisites

Please make sure following prerequisites are all installed.

 - python
 - pip
 - PostgreSQL server
 - psql

### install virtualenv

Please following the instructions in https://virtualenv.pypa.io/en/stable/installation/ to install virtualenv first.

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
DATABASE_URI=postgresql://localhost/airmnb
```

A more general pattern will be:
```
DATABASE_URI=postgresql://username:password@hostname:port/database_name
```

#### initialize database for database migration

This step is only needed for the first time after installation.

```
python manage.py db init
```

#### run database migration script

```
python manage.py db upgrade head
```