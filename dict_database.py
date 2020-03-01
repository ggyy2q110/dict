"""
dict数据处理模块
"""
import pymysql


class DictDatabase:
    def __init__(self):
        self.host = "192.168.139.133"
        self.port = 3306
        self.user = "admin"
        self.password = "123456"
        self.database = "dict"
        self.charset = "utf8"
        self.conn_database()

    def conn_database(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  database=self.database,
                                  charset=self.charset)

    def create_cur(self):
        self.cur = self.db.cursor()

    def add_user(self, username, password):
        sql = "select name from user where name = %s;"
        num = self.cur.execute(sql, [username])
        if num:
            return False
        else:
            try:
                insert_sql = "insert into user (name,password) values(%s,%s);"
                self.cur.execute(insert_sql, [username, password])
                self.db.commit()
                return True
            except:
                self.db.rollback()

    def dict_login(self, username, password):
        sql = "select name,password from user where name = %s and password = %s;"
        num = self.cur.execute(sql, [username, password])
        if num:
            return True
        else:
            return False

    def dict_list_word(self, word, username):
        sql = "select id from user where name = %s;"
        self.cur.execute(sql, [username])
        info = self.cur.fetchone()[0]
        try:
            insert_sql = "insert into history (word,u_id) values (%s,%s);"
            self.cur.execute(insert_sql, [word, info])
            self.db.commit()
        except:
            self.db.rollback()
        list_sql = "select mean from words where word = %s;"
        self.cur.execute(list_sql, [word])
        data = self.cur.fetchone()
        if data:
            return data
        else:
            return False

    def dict_list_history(self, username):
        sql = "select word,time from history where u_id = (select id from user where name = %s) limit 10; "
        self.cur.execute(sql, [username])
        info = self.cur.fetchall()
        return info
