import pandas as pd
import mysql.connector as connection
from sqlalchemy import create_engine

class DB:
    def __init__(self, creds):
        self.host = creds['host']
        self.database = creds['database']
        self.user = creds['user']
        self.passwd = creds['passwd']
        self.type = creds['type']

    def read_sql(self, sql, **kwargs):
        if self.type == 'mysql':
            db = connection.connect(host = self.host, database = self.database, user = self.user, passwd = self.passwd)
        elif self.type == 'postgres':
            db = create_engine('postgresql://{user}:{password}@{host}/{database}'.format(
                user = self.user,
                password = self.passwd,
                host = self.host,
                database = self.database
            )).connect()
        data = pd.read_sql(sql, db, **kwargs)
        db.close()

        return data
