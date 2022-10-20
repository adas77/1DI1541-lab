#!/usr/bin/python
from datetime import datetime
import sqlite3


class Database:
    def __init__(self, filename: str):
        self.filename = filename

    def __connect_to_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.filename)
        return conn

    def user_create(self):
        try:
            conn = self.__connect_to_db()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY NOT NULL, nickname TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, reg_date timestamp)")
            conn.commit()
            print("user table created successfully")
        except:
            print("user table creation failed")
        finally:
            conn.close()

    def user_insert(self, user):
        inserted_user = {}
        try:
            conn = self.__connect_to_db()
            cur = conn.cursor()
            cur.execute("""SELECT email ,nickname FROM user WHERE email=? OR nickname=?""",
                        (user['email'], user['nickname']))
            result = cur.fetchone()
            if result:
                print("nickname or email already exists")
            else:
                cur.execute("INSERT INTO user (nickname, email, password, reg_date) values (?, ?, ?, ?)",
                            (user['nickname'], user['email'], user['password'], datetime.now()))
            conn.commit()
            inserted_user = self.user_get_by_id(cur.lastrowid)
            print(inserted_user)

        except:
            conn.rollback()

        finally:
            conn.close()

        return inserted_user

    def user_get_by_id(self, user_id):
        user = {}
        try:
            conn = self.__connect_to_db()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM user WHERE user_id = ?",
                        (user_id,))
            row = cur.fetchone()
            user["user_id"] = row["user_id"]
            user["nickname"] = row["nickname"]
            user["email"] = row["email"]
            user["password"] = row["password"]
            user["reg_date"] = row["reg_date"]
        except:
            user = {}
        return user

    def user_handle_login(self, user) -> bool:
        passed = False
        try:
            conn = self.__connect_to_db()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            print(user)

            cur.execute("SELECT * FROM user WHERE email = ? ",
                        (user['email'],))
            row = cur.fetchone()
            print("aaa")
            print(row)
            if row and row["password"] == user["password"]:
                print("You logged in")
                passed = True

            else:
                print("You not logged in")
        except:
            print("fail")
        return passed

    def users_get(self):
        users = []
        try:
            conn = self.__connect_to_db()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM user")
            rows = cur.fetchall()
            for i in rows:
                user = {}

                user["user_id"] = i["user_id"]
                user["nickname"] = i["nickname"]
                user["email"] = i["email"]
                user["password"] = i["password"]
                user["reg_date"] = i["reg_date"]

                users.append(user)

        except:
            users = []

        return users
