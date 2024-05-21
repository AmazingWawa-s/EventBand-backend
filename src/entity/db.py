#from django.db import connection
import pymysql


class DB():
    def __init__(self) -> None:
        self.conn=pymysql.connect(host="192.168.43.246",user="sa",password="",db="eventband",port=3306,charset="utf8")
        self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    def get(self):
        return self.cursor.fetchall()
    def rollback(self):
        self.cursor.rollback()
    
    
    def __del__(self):
        self.cursor.close()
    #虚函数select
    def select(self,table):
        raise NotImplementedError
    

class UserDB(DB):
    def __init__(self):
        super().__init__()
    def selectById(self,attrs,id):
        self.cursor.execute("select %s from user where user_id =%s",[attrs,id])
    def selectByName(self,attrs,name):
        self.cursor.execute("select %s from user where user_name =%s",[attrs,name])
    
    def delete(self,id):
        self.cursor.execute("delete from user where user_id=%s",id)
        self.conn.commit()
    def insertNewUser(self,name,password):
        self.cursor.execute("insert into user (user_name,user_password) values (%s,%s)",[name,password])
        self.conn.commit()
    def update(self,id,toset):
        self.cursor.execute("update user set "+toset+"where user_id=%s",id)
        self.conn.commit()
        
        
        
    