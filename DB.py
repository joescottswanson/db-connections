import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus


class DB:
    def __init__(self, creds):
        self.host = creds["host"] if "host" in creds else ""
        self.database = creds["database"] if "database" in creds else ""
        self.user = creds["user"] if "user" in creds else ""
        self.passwd = creds["passwd"] if "passwd" in creds else ""
        self.type = creds["type"] if "type" in creds else ""
        self.account_identifier = (
            creds["account_identifier"] if "account_identifier" in creds else ""
        )
        self.schema = creds["schema"] if "schema" in creds else ""
        self.warehouse = creds["warehouse"] if "warehouse" in creds else ""
        self.role = creds["role"] if "role" in creds else ""
        self.private_key_file = creds.get("private_key_file", "")
        self.private_key_file_pwd = creds.get("private_key_file_pwd", "")

    def read_sql(self, sql, **kwargs):
        """
        A wrapper function around pandas's read_sql method. Simply passes the
        kwargs along to pandas.read_sql, and uses the connection to the DB
        established by this class to run the query.
        """
        if self.type == "mysql":
            d_b = create_engine(
                f"mysql://{self.user}:{quote_plus(self.passwd)}"
                + f"@{self.host}/{self.database}"
            ).connect()
        elif self.type == "postgres":
            d_b = create_engine(
                f"postgresql://{self.user}:{quote_plus(self.passwd)}"
                + f"@{self.host}/{self.database}"
            ).connect()
        elif self.type == "snowflake":
            url = (
                f"snowflake://{self.user}@{self.account_identifier}/"
                f"{self.database}/{self.schema}?warehouse={self.warehouse}&role={self.role}"
            )
            if self.private_key_file:
                connect_args = {
                    "authenticator": "SNOWFLAKE_JWT",
                    "private_key_file": self.private_key_file,
                }
                if self.private_key_file_pwd:
                    connect_args["private_key_file_pwd"] = self.private_key_file_pwd
                d_b = create_engine(url, connect_args=connect_args).connect()
            else:
                d_b = create_engine(url + "&authenticator=externalbrowser").connect()
        data = pd.read_sql(sql, d_b.connection, **kwargs)
        d_b.close()

        return data
