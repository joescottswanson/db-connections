import pandas as pd
import mysql.connector as connection
from sqlalchemy import create_engine

class DB:
    def __init__(self, creds):
        self.host = creds['host'] if 'host' in creds else ''
        self.database = creds['database'] if 'database' in creds else ''
        self.user = creds['user'] if 'user' in creds else ''
        self.passwd = creds['passwd'] if 'passwd' in creds else ''
        self.type = creds['type'] if 'type' in creds else ''
        self.account_identifier = creds['account_identifier'] \
            if 'account_identifier' in creds else ''
        self.schema = creds['schema'] if 'schema' in creds else ''
        self.warehouse = creds['warehouse'] if 'warehouse' in creds else ''
        self.role = creds['role'] if 'role' in creds else ''

    def read_sql(self, sql, **kwargs):
        '''
        A wrapper function around pandas's read_sql method. Simply passes the
        kwargs along to pandas.read_sql, and uses the connection to the DB
        established by this class to run the query.
        '''
        if self.type == 'mysql':
            d_b = connection.connect(host=self.host,
                                     database=self.database,
                                     user=self.user,
                                     passwd=self.passwd)
        elif self.type == 'postgres':
            d_b = create_engine(f'postgresql://{self.user}:{self.passwd}' +
                                f'@{self.host}/{self.database}').connect()
        elif self.type == 'snowflake':
            d_b = create_engine(f'snowflake://{self.user}:{self.passwd}' +
                                f'@{self.account_identifier}/' +
                                f'{self.database}/{self.schema}?' +
                                f'warehouse={self.warehouse}&role={self.role}'
                                ).connect()
        data = pd.read_sql(sql, d_b, **kwargs)
        d_b.close()

        return data
