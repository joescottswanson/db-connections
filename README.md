# DB Connections
This repo provides a DB Factory class for getting connections to Mysql and Postgres DBs and reading queries with pandas. It's really
just a wrapper around mysql.connector, sqlalchemy's engine, and pandas's read_sql method.

You'll put together a `settings.py` file modeled after `settings.template.py` where you'll define the credentials and 
names for the different DBs you want to connect to. Then using it is as simple as:

```
from DBFactory import DBFactory

dbs = DBFactory()
db = dbs.getDb('example_mysql_db')

data = db.read_sql('select * from table') # returns a pandas dataframe
```

I've used it with jupyter notebooks for data analysis.

# Installation and Requirements
There is a bloated requirements.txt file included which will allow you to use this with all of Python's basic data
analysis packages (pandas, jupyter, matplotlib, etc.). You should be able to install with:
`pip install -r requirements.txt`

I haven't tested this and it might not be that easy!
