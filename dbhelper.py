import sqlite3


class Dbhelper ():

    def __init__(self):
        self.dblocation = '../database.db'
        self.connection = sqlite3.connect(self.dblocation)
        self.cursor = self.connection.cursor()

    def authorized(self, uid):
        with self.connection:
            self.cursor.execute("""SELECT id FROM users WHERE id = ?""",
                (uid,))
        if self.cursor.fetchone() == None:
            return False
        else:
            return True

    def getapitoken(self):
        with self.connection:
            self.cursor.execute("""select value from configuration WHERE name = 'api_token'""")
            return self.cursor.fetchone()[0]


if __name__ == '__main__':
    dbhelper = Dbhelper()
    TOKEN = dbhelper.getapitoken()
    print (TOKEN)
