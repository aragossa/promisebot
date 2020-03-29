import datetime
import sqlite3
import uuid


def getapitoken():
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
    with connection:
        cursor.execute("""SELECT value FROM configuration WHERE name = 'api_token'""")
        return cursor.fetchone()[0]


def resetusersstate():
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
    with connection:
        cursor.execute("""UPDATE users_stat SET state = 'MAIN_MENU' WHERE state IS NOT NULL""")
        cursor.execute("""UPDATE users_stat SET selected_user = '' WHERE selected_user IS NOT NULL""")


class Botuser():

    def __init__(self, uid):
        self.uid = uid
        self.dblocation = 'data/database.db'
        self.connection = sqlite3.connect(self.dblocation)
        self.cursor = self.connection.cursor()

    def isauthorized(self):
        with self.connection:
            self.cursor.execute("""SELECT id FROM users WHERE id = ?""",
                                (self.uid,))
        if self.cursor.fetchone():
            return True
        else:
            return False

    def isadmin(self):
        with self.connection:
            self.cursor.execute("""SELECT group_id FROM users WHERE id = ?""",
                                (self.uid,))
        result = self.cursor.fetchone()
        if result:
            if str(result[0]) == str(self.uid):
                return True
            else:
                return False
        else:
            return False

    def getusertype(self):
        with self.connection:
            self.cursor.execute("""SELECT group_id FROM users WHERE id = ?""",
                                (self.uid,))
        result = self.cursor.fetchone()

        if str(result[0]) == str(self.uid):
            return 'admin'
        else:
            return 'user'

    def getusername(self):
        with self.connection:
            self.cursor.execute("""SELECT username FROM users_stat WHERE id = ?""",
                                (self.uid,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return result

    def getgroupusers(self):
        userlist = []
        with self.connection:
            self.cursor.execute("""SELECT id FROM users WHERE group_id = (SELECT group_id FROM users WHERE id = ?)""",
                                (self.uid,))
        for tmpuser in self.cursor.fetchall():
            curuser = Botuser(tmpuser[0])
            userlist.append({
                'id': tmpuser[0],
                'username': curuser.getusername()
            })
        return userlist

    def getuserstat (self, userid):
        with self.connection:
            self.cursor.execute("""SELECT * FROM users_stat WHERE id = ?""",
                                (userid,))
            result = self.cursor.fetchone()
            return result


    def getuserstate(self):
        with self.connection:
            self.cursor.execute("""SELECT state FROM users_stat WHERE id = ?""",
                                (self.uid,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return result

    def updateuserstate(self, newstate):
        with self.connection:
            self.cursor.execute("""UPDATE users_stat SET state = ? WHERE id = ?""",
                                (newstate, self.uid,))

    def resetuserstate(self):
        connection = sqlite3.connect('data/database.db')
        cursor = connection.cursor()
        with connection:
            cursor.execute("""UPDATE users_stat SET state = 'MAIN_MENU' WHERE id = ?""", (self.uid,))
            cursor.execute("""UPDATE users_stat SET selected_user = '' WHERE id = ?""", (self.uid,))
            cursor.execute("""UPDATE users_stat SET selected_promise = '' WHERE id = ?""", (self.uid,))

    def updateselecteduser(self, selecteduser):
        with self.connection:
            self.cursor.execute("""UPDATE users_stat SET selected_user = ? WHERE id = ?""",
                                (selecteduser, self.uid,))

    def getuserselecteduser(self):
        with self.connection:
            self.cursor.execute("""SELECT selected_user FROM users_stat WHERE id = ?""",
                                (self.uid,))
            result = self.cursor.fetchone()
            return result[0]

    def updateselectedpromise(self, selectedpromise):
        with self.connection:
            self.cursor.execute("""UPDATE users_stat SET selected_promise = ? WHERE id = ?""",
                                (selectedpromise, self.uid,))

    def getuserselectedpromise(self):
        with self.connection:
            self.cursor.execute("""SELECT selected_promise FROM users_stat WHERE id = ?""",
                                (self.uid,))
            result = self.cursor.fetchone()
            return result[0]

    def insertrequest(self, request, selecteduser):
        with self.connection:
            self.cursor.execute("""INSERT INTO promises (id, request_text, promise_date, promise_status, user_id_give, user_id_get, creation_date, remindes_count)
                                   VALUES (?, ?, 'Без даты', 'NEW', ?, ?, datetime('now', 'localtime'), 0);""",
                                (str(uuid.uuid4()), request, selecteduser, self.uid,))
            self.cursor.execute("""SELECT id, max(creation_date) FROM promises WHERE user_id_get = ?""",
                                (self.uid,))
            result = self.cursor.fetchone()[0]
            return result

    def getlastrequest(self):
        with self.connection:
            self.cursor.execute("""SELECT id, max(creation_date) FROM promises WHERE user_id_get = ?""",
                                (self.uid,))
            result = self.cursor.fetchone()[0]
            return result

    def updaterequestdate(self, promiseid, promisedate):
        with self.connection:
            self.cursor.execute("""UPDATE promises SET promise_date = ? WHERE id = ?""",
                                (promisedate, promiseid,))

    def getrequestinfo(self, requestid):
        with self.connection:
            self.cursor.execute(
                """SELECT request_text, promise_text, promise_date, user_id_get, user_id_get FROM promises WHERE id = ?""",
                (requestid,))
            result = self.cursor.fetchone()
            return result

    def requestreject(self, requestid):
        with self.connection:
            self.cursor.execute("""UPDATE promises SET promise_status = 'REJECT' WHERE id = ?""",
                                (requestid,))
            self.cursor.execute("""UPDATE
                                        users_stat
                                   SET
                                        trust = trust - (SELECT value FROM settings WHERE name = 'REJECT_REQUEST' AND group_id = (SELECT group_id FROM users WHERE id = ?))
                                   WHERE
                                        id = ?""",
                                (self.uid, self.uid,))
            self.cursor.execute("""SELECT user_id_give, user_id_get, request_text FROM promises WHERE id = ?""",
                                (requestid,))
            return self.cursor.fetchone()

    def requestaccept(self, requestid, promisetext):
        with self.connection:
            self.cursor.execute("""UPDATE promises SET promise_status = 'ACCEPT' WHERE id = ?""",
                                (requestid,))
            self.cursor.execute("""UPDATE promises SET promise_text = ? WHERE id = ?""",
                                (promisetext, requestid,))
            self.cursor.execute("""SELECT user_id_give, user_id_get, promise_text FROM promises WHERE id = ?""",
                                (requestid,))
            return self.cursor.fetchone()

    """ Обещания и запросы, где получатель user"""

    def getactivepromisesme(self):
        with self.connection:
            self.cursor.execute("""SELECT id, request_text, promise_text, promise_date, user_id_give
                                   FROM promises
                                   WHERE promise_status = 'ACCEPT'
                                   AND user_id_get = ?""",
                                (self.uid,))
            return self.cursor.fetchall()

    def getununsweredrequestsme(self):
        with self.connection:
            self.cursor.execute("""SELECT id, request_text, promise_text, promise_date, user_id_give
                                   FROM promises
                                   WHERE promise_status = 'NEW'
                                   AND user_id_get = ?""",
                                (self.uid,))
            return self.cursor.fetchall()

    """ Обещания и запросы, где отправитель user"""

    def getactivepromisesmy(self):
        with self.connection:
            self.cursor.execute("""SELECT id, request_text, promise_text, promise_date, user_id_get
                                   FROM promises
                                   WHERE promise_status = 'ACCEPT'
                                   AND user_id_give = ?""",
                                (self.uid,))
            return self.cursor.fetchall()

    def getununsweredrequestsmy(self):
        with self.connection:
            self.cursor.execute("""SELECT id, request_text, promise_text, promise_date, user_id_get
                                   FROM promises
                                   WHERE promise_status = 'NEW'
                                   AND user_id_give = ?""",
                                (self.uid,))
            return self.cursor.fetchall()


    def promisefin(self, promiseid, action):
        with self.connection:
            if action == 'accept':
                promisestatus = 'COMPLITE'
                self.cursor.execute("""UPDATE users_stat SET trust = trust + (SELECT value FROM settings WHERE name = 
                'COMPLITE_PROMISE' AND group_id = (SELECT group_id FROM users WHERE id = ?)) WHERE id = ?""",
                                    (self.uid, self.uid,))
            elif action == 'break':
                promisestatus = 'BREAK'
                self.cursor.execute("""UPDATE users_stat SET trust = trust - (SELECT value FROM settings WHERE name = 
                'BREAK_PROMISE' AND group_id = (SELECT group_id FROM users WHERE id = ?)) WHERE id = (SELECT 
                user_id_give FROM promises WHERE id = ?)""",
                                    (self.uid, promiseid,)
                                    )
            self.cursor.execute("""UPDATE promises SET promise_status = ? WHERE id = ?""",
                                (promisestatus, promiseid,))


    def getsetting (self):
        with self.connection:
            self.cursor.execute("""SELECT * FROM settings WHERE group_id = (SELECT group_id FROM users WHERE id = ?)""",
                                (self.uid,))
            return self.cursor.fetchall()

    def resetstatistics (self):
        with self.connection:
            self.cursor.execute("""UPDATE users_stat
                                    SET likes = 0, dislikes = 0, trust = 50
                                    WHERE id IN (SELECT id FROM users WHERE group_id = (SELECT group_id FROM users WHERE id = ?));""",
                                (self.uid,))
            return self.cursor.fetchall()


    def updatesetting (self, parameter, value):
        with self.connection:
            self.cursor.execute("""UPDATE settings
                                    SET value = ?
                                    WHERE name = ?
                                    AND group_id = (SELECT group_id FROM users WHERE id = ?);""",
                                (value, parameter, self.uid,))
            return self.cursor.fetchall()




if __name__ == '__main__':
    user = Botuser('556047985')
    promiseid='2a3e4970-f9bc-41ce-942c-00d34b76b796'
    print(user.resetstatistics())
