# flask-app


## Setup Development Environment

### Prerequisites

Please make sure following prerequisites are all installed.

 - python
 - pip
 - PostgreSQL server
 - psql

### Install virtualenv

Please follow the instructions in https://virtualenv.pypa.io/en/stable/installation/ to install virtualenv first.

### Clone code repo and install dependencies

```
$ git clone https://github.com/cg1101/flask-app

$ cd flask-app

$ virtualenv venv

$ . venv/bin/activate

$ pip install -r requirements.txt
```

### Setup Database

#### Create database

Plese use following command to create database
```
createdb myappdb
```

#### Setup db uri

Edit setenv.sh, set the ```DATABASE_URI``` to following value

```
export DATABASE_URI=postgresql://localhost/myappdb
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


#### Initialize database for database migration

If you just created database, it hasn't been initialized yet. Run following command:

```
python manage.py db downgrade base
```

This step is only needed for the first time after installation. It will create a table in public schema called 'alembic_version'. If 
you have run this before, then you shouldn't run this command again, otherwise the existing data will be wiped out.

#### Run database migration script

You may upgrade the db schema to the latest version by running:
```
python manage.py db upgrade head
```

### Add convenience commands

For your convenience, you can create an alias command in your .bash_profile to quickly jump to your working folder. For example, if you have cloned the repo to `~/flask-app` and you want to use a shortcut `aa`, then you can add:

```
alias aa='cd ~/flask-app; . venv/bin/activate; . setenv.sh'
```

### Start server

After you have setup database, you can start the server by running:
```
python manage.py runserver
```

### Test api

When server is running, you can test api by running:
```
curl localhost:5000/health-check
```

This should return status code 200 and a text says 'OK'.

Or you can test api endpoint by running:
```
curl localhost:5000/api/1.0/users/
```

If users table is empty, you will get an empty list:
```
{
  "users": []
}
```

You can add a user into users table and try this api again, it should return the user you just created, for example:
```
echo "insert into users values ('e0a5d16c-3bed-11e8-b467-0ed5f89f718b', 'John', 'Smith', 'male', '1970-01-01', 'jsmith@company.com', 'unknown', NULL, now());" | psql ${DATABASE_URI}
```
Then you will get:
```
{
  "users": [
    {
      "avartar": null, 
      "createdAt": "2018-04-09T12:09:57.489351+00:00", 
      "dob": "1970-01-01", 
      "email": "jsmith@company.com", 
      "familyName": "John", 
      "gender": "male", 
      "givenName": "Smith", 
      "userId": "e0a5d16c-3bed-11e8-b467-0ed5f89f718b"
    }
  ]
}
```
