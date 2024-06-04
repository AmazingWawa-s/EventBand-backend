import pymysql

class DB():
    def __init__(self):
        self.conn=pymysql.connect(host="192.168.43.246",user="sa",password="",db="eventband",port=3306,charset="utf8")
        self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        #self.conn=connection.connect(host="192.168.43.246",user="sa",password="",db="eventband",port=3306,charset="utf8")
        #self.cursor=connection.cursor()
    def get(self):
        return self.cursor.fetchall()
    def rollback(self):
        self.cursor.rollback()
    
    
    
    def __del__(self):
        self.cursor.close()
    

class UserDB(DB):
    def __init__(self):
        super().__init__()
    def selectById(self,attrs,id):
        self.cursor.execute("select "+ attrs +" from user where user_id ="+str(id))
    def selectByName(self,attrs,name):
        self.cursor.execute("select * from user where user_name =%s",name)
    def select(self,attrs,nid):
        if type(nid) is int:
            self.cursor.execute("select "+ attrs +" from user where user_id ="+str(nid))
        elif type(nid) is str:
            self.cursor.execute("select "+ attrs +" from user where user_name ="+nid)
    def selectAll(self,attrs):
        self.cursor.execute("select * from user where user_name =%s")

    def deleteUser(self,id):
        self.cursor.execute("delete from user where user_id=%s",id)
        self.conn.commit()
    def insertNewUser(self,name,password):
        self.cursor.execute("insert into user (user_name,user_password) values (%s,%s)",[name,password])
        self.conn.commit()
    def updateUser(self,id,toset):
        self.cursor.execute("update user set "+toset+" where user_id="+str(id))
        #self.cursor.execute("update user set (%s) where user_id=%s",(toset,id))
        self.conn.commit()
        

class EventDB(DB):
    def __init__(self):
        super().__init__()
    def checkCollision1(self,location,date,start,end):
        self.cursor.execute("select elrelation_id from elrelation where elrelation_date=%s and elrelation_location_id=%s and elrelation_start>=%s and elrelation_start<=%s",[date,location,start,end])
    def checkCollision2(self,location,date,start,end):
        self.cursor.execute("select elrelation_id from elrelation where elrelation_date=%s and elrelation_location_id=%s and elrelation_end>=%s and elrelation_end<=%s",[date,location,start,end])
    def checkCollision3(self,location,date,start,end):
        self.cursor.execute("select elrelation_id from elrelation where elrelation_date=%s and elrelation_location_id=%s and elrelation_start<=%s and elrelation_end>=%s",[date,location,start,end])
    def selectAll(self,attrs):
        self.cursor.execute("select "+attrs+" from event_brief")
    def selectById(self,attrs,id):
        self.cursor.execute("select "+ attrs +" from event_brief where event_id ="+str(id))
    def selectByIds(self,attrs,ids):
        self.cursor.execute("select "+ attrs +" from event_brief where event_id in (" + ids + ")")
    def selectEUByUserIdRole(self,attrs,id,role):
        self.cursor.execute("select distinct "+ attrs +" from eurelation where eurelation_user_id ="+str(id)+" and eurelation_role="+str(role))
    def selectEUByEventId(self,attrs,id):
        self.cursor.execute("select distinct "+ attrs +" from eurelation where eurelation_event_id ="+str(id))
    
    def insertEU(self,event_id,user_id,role):
        self.cursor.execute("insert into eurelation (eurelation_event_id,eurelation_user_id,eurelation_role) values(%s,%s,%s)",[event_id,user_id,role])
        self.conn.commit()
    def insertEvent(self,toinsert):
        self.cursor.execute("insert into event_brief " + toinsert)
        self.conn.commit()
    def insertEL(self,event_id,location_id,date,start,end):
        self.cursor.execute("insert into elrelation (elrelation_event_id,elrelation_location_id,elrelation_date,elrelation_start,elrelation_end) values(%s,%s,%s,%s,%s)",[event_id,location_id,date,start,end])
        self.conn.commit()
    # def delete(self,id):
    #     self.cursor.execute("delete from user where user_id=%s",id)
    #     self.conn.commit()
    def updateEvent(self,id,toset):
        self.cursor.execute("update event_brief set "+toset+" where event_id="+str(id))
        #self.cursor.execute("update user set (%s) where user_id=%s",(toset,id))
        self.conn.commit()
    def getLastEventId(self):
        self.cursor.execute("select event_id from event_brief order by event_id desc limit 1")

    def deleteEventById(self,id):
        self.cursor.execute("delete from event_brief where event_id=%s",id)
        self.conn.commit()
    def deleteEUByEventId(self,event_id):
        self.cursor.execute("delete from eurelation where eurelation_event_id=%s and eurelation_role=1",event_id)
        self.conn.commit()
    def deleteEUByUserId(self,user_id):
        self.cursor.execute("delete from eurelation where eurelation_user_id=%s and eurelation_role=1",user_id)
        self.conn.commit()
          
class LocationDB(DB):
    def __init__(self):
        super().__init__()
        
    def selectLocationById(self,attrs,id):
        self.cursor.execute("select "+ attrs +" from location where location_id ="+str(id))
    
    def selectAllLocations(self,attrs):
        self.cursor.execute("select "+attrs+" from location")
        
    def insertNewLocation(self,lid,firstname,name,description,capacity,type):
        self.cursor.execute("insert into location (location_id,location_firstname,location_name,location_description,location_capacity,location_type) values (%s,%s,%s,%s,%s,%s)",[lid,firstname,name,description,capacity,type])
        self.conn.commit()
    def updateLocation(self,id,toset):
        self.cursor.execute("update location set "+toset+" where location_id="+str(id))
        #self.cursor.execute("update user set (%s) where user_id=%s",(toset,id))
        self.conn.commit()
    def getLastLocationId(self):
        self.cursor.execute("select location_id from location order by location_id desc limit 1")
    def deleteLocationById(self,id):
        self.cursor.execute("delete from location where location_id=%s",id)
        self.cursor.execute("delete from elrelation where elrelation_location_id=%s",id)
        self.conn.commit()