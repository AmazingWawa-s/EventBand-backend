from django.db import connection
import pymysql

class DB():
    def __init__(self) -> None:
        self.conn=pymysql.connect(host="192.168.43.246",user="sa",password="",db="eventband",port=3306,charset="utf8")
        self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        #self.conn=connection.connect(host="192.168.43.246",user="sa",password="",db="eventband",port=3306,charset="utf8")
        #self.cursor=connection.cursor()
    def get(self):
        return self.cursor.fetchall()
    def rollback(self):
        self.cursor.rollback()
    
    #虚函数select
    def select(self,table):
        raise NotImplementedError
    def __del__(self):
        self.cursor.close()
    

class UserDB(DB):
    def __init__(self):
        super().__init__()
    def selectById(self,attrs,id):
        self.cursor.execute("select "+ attrs +" from user where user_id ="+str(id))
    def selectByName(self,attrs,name):
        self.cursor.execute("select * from event where user_name =%s",name)
    def select(self,attrs,nid):
        if type(nid) is int:
            self.cursor.execute("select "+ attrs +" from user where user_id ="+str(nid))
        elif type(nid) is str:
            self.cursor.execute("select "+ attrs +" from user where user_name ="+nid)
    def selectAll(self,attrs):
        self.cursor.execute("select * from event where user_name =%s",name)

    def delete(self,id):
        self.cursor.execute("delete from user where user_id=%s",id)
        self.conn.commit()
    def insertNewUser(self,name,password):
        self.cursor.execute("insert into user (user_name,user_password) values (%s,%s)",[name,password])
        self.conn.commit()
    def update(self,id,toset):
        self.cursor.execute("update user set "+toset+" where user_id="+str(id))
        #self.cursor.execute("update user set (%s) where user_id=%s",(toset,id))
        self.conn.commit()
        

class EventDB(DB):
    def __init__(self):
        super().__init__()
    def selectById(self,attrs,id):
        self.cursor.execute("select "+ attrs +" from event where event_id ="+str(id))
    def selectByName(self,attrs,name):
        self.cursor.execute("select * from user where event_name =%s",name)
    def select(self,attrs,nid):
        if type(nid) is int:
            self.cursor.execute("select "+ attrs +" from user where user_id ="+str(nid))
        elif type(nid) is str:
            self.cursor.execute("select "+ attrs +" from user where user_name ="+nid)
        
    def delete(self,id):
        self.cursor.execute("delete from user where user_id=%s",id)
        self.conn.commit()
    def insertNewUser(self,name,password):
        self.cursor.execute("insert into user (user_name,user_password) values (%s,%s)",[name,password])
        self.conn.commit()
    def update(self,id,toset):
        self.cursor.execute("update user set "+toset+" where user_id="+str(id))
        #self.cursor.execute("update user set (%s) where user_id=%s",(toset,id))
        self.conn.commit()       
        
    