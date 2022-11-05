#!/usr/bin/python
from datetime import datetime
import sqlite3


class Database:
    def __init__(self, filename: str):
        self.filename = filename

    def __connect_to_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.filename)
        return conn


# user


    def user_drop(self):
        try:
            conn = self.__connect_to_db()
            conn.execute(
                "DROP TABLE user")
            conn.commit()
            print("user table dropped successfully")
        except:
            print("user table drop failed")
        finally:
            conn.close()

    def user_delete_all(self):
        try:
            conn = self.__connect_to_db()
            conn.execute(
                "DELETE FROM user")
            conn.commit()
            print("user table cleared successfully")
        except:
            print("user table clear failed")
        finally:
            conn.close()

    def user_create(self):
        try:
            conn = self.__connect_to_db()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY NOT NULL, nickname TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL, password BINARY(16) NOT NULL, reg_date timestamp)")
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
                return "Nickname or email already exists", 444
            else:
                cur.execute("INSERT INTO user (nickname, email, password, reg_date) values (?, ?, ?, ?)",
                            (user['nickname'], user['email'], user['password'], datetime.now()))
            conn.commit()
            inserted_user = self.user_get_by_id(cur.lastrowid)
            print(inserted_user)
            inserted_user['password'] = 'SECRET'

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

    def user_get_by_email(self, email):
        user = {}
        try:
            conn = self.__connect_to_db()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM user WHERE email = ?",
                        (email,))
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

    def users_update(self, user_id, password):
        updated_user = {}
        try:
            conn = self.__connect_to_db()
            cur = conn.cursor()

            cur.execute("UPDATE user SET password = ? WHERE user_id = ?", (
                password, user_id
            ))

            conn.commit()
            updated_user = self.user_get_by_id(user_id)
            print(updated_user)

        except:
            conn.rollback()
            updated_user = {}
        finally:
            conn.close()

        return updated_user

    def users_change_password(self, email, password):
        updated_user = {}
        try:
            conn = self.__connect_to_db()
            cur = conn.cursor()

            cur.execute("UPDATE user SET password = ? WHERE email = ?", (
                password, email
            ))

            conn.commit()
            updated_user = self.user_get_by_email(email)
            print(updated_user)

        except:
            conn.rollback()
            updated_user = {}
        finally:
            conn.close()

        return updated_user


# product

    def product_create(self):
        try:
            conn = self.__connect_to_db()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY NOT NULL,img TEXT NOT NULL, price DECIMAL(10,2) NOT NULL, quantity INTEGER NOT NULL, description TEXT,  reg_date timestamp)")
            conn.commit()
            print("product table created successfully")
        except:
            print("product table creation failed")
        finally:
            conn.close()

    def product_insert(self, product):
        inserted_product = {}
        try:
            conn = self.__connect_to_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO product (img, price, quantity, description,reg_date) values (?, ?, ?, ?, ?)",
                        (product['img'], product['price'], product['quantity'], product['description'], datetime.now()))
            conn.commit()
            inserted_product = self.product_get_by_id(cur.lastrowid)
            print(inserted_product)

        except:
            conn.rollback()

        finally:
            conn.close()

        return inserted_product

    def product_get_by_id(self, product_id):
        product = {}
        try:
            conn = self.__connect_to_db()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM product WHERE product_id = ?",
                        (product_id,))
            row = cur.fetchone()
            # "CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY NOT NULL,img TEXT NOT NULL, price DECIMAL(10,2) NOT NULL, quantity INTEGER NOT NULL, description TEXT,  reg_date timestamp)"
            product["product_id"] = row["product_id"]
            product["img"] = row["img"]
            product["price"] = row["price"]
            product["quantity"] = row["quantity"]
            product["description"] = row["description"]
            product["reg_date"] = row["reg_date"]
        except:
            product = {}
        return product

    def products_get(self):
        products = []
        try:
            conn = self.__connect_to_db()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            for i in rows:
                product = {}

                product["product_id"] = i["product_id"]
                product["img"] = i["img"]
                product["price"] = i["price"]
                product["quantity"] = i["quantity"]
                product["description"] = i["description"]
                product["reg_date"] = i["reg_date"]

                products.append(product)

        except:
            products = []

        return products
