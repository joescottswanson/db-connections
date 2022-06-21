import settings
import DB

class DBFactory:
    def __init__(self):
        self.creds = settings.db_creds

    def getDb(self, name):
        return DB.DB(self.creds[name])
