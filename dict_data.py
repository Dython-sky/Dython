# 定义一个信息类
import pymysql

class Database:
    def __init__(self,host= "localhost",port =3306,user=None,password=None,database =None,charset = 'utf8'):
        self.db = pymysql.connect(host=host,
                     port=port ,
                     user=user,
                     password=password,
                     database=database,
                     charset=charset)
        self.cur = self.db.cursor()
    def register(self,name,password):
        # 判断用户是否存在
        sql = "select name from user where name='%s';" % name
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return False
        try:
            exe = [name,password]
            sql = "insert into user (name,password) values (%s,%s);"
            self.cur.execute(sql, exe)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
    def login(self,account,password):
        # 判断用户是否存在
        sql = "select id,password from user where id=%s and password=%s;"
        self.cur.execute(sql, [account, password])
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False
    def gain_word(self,word):
        sql = 'select mean from words where word = %s'
        self.cur.execute(sql,word)
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return False
    def insert_record(self,word,account):
        sql = 'insert into hist2 (word,user_id) values (%s,%s)'
        self.cur.execute(sql,[word,account])
        self.db.commit()
    def take_record(self,account):
        sql = 'select word,time from hist2 where user_id = %s order by time desc limit 10;'
        print(sql)
        self.cur.execute(sql,account)
        result = self.cur.fetchall()
        print(result)
        if result:
            return str(result)
        else:
            return False

