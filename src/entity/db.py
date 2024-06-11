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
        self.cursor.execute("select "+ attrs +' from user where user_name ="'+str(name)+'"')
    def select(self,attrs,nid):
        if type(nid) is int:
            self.cursor.execute("select "+ attrs +" from user where user_id ="+str(nid))
        elif type(nid) is str:
            self.cursor.execute("select "+ attrs +' from user where user_name ="'+nid+'"')
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
    def checkCollision(self,location,start_date,end_date,start_time,end_time):
        self.cursor.execute("select elrelation_id from elrelation where elrelation_location_id=%s and not elrelation_start_date>%s and not elrelation_end_date<%s and not elrelation_start_time>%s and not elrelation_end_time<%s",[location,end_date,start_date,end_time,start_time])
    def checkCollision1(self,location,date,start,end):
        self.cursor.execute("select elrelation_id from elrelation where elrelation_date=%s and elrelation_location_id=%s and elrelation_start>=%s and elrelation_start<=%s",[date,location,start,end])
    def checkCollision2(self,location,date,start,end):
        self.cursor.execute("select elrelation_id from elrelation where elrelation_date=%s and elrelation_location_id=%s and elrelation_end>=%s and elrelation_end<=%s",[date,location,start,end])
    def checkCollision3(self,location,date,start,end):
        self.cursor.execute("select elrelation_id from elrelation where elrelation_date=%s and elrelation_location_id=%s and elrelation_start<=%s and elrelation_end>=%s",[date,location,start,end])
    def selectAllEvents(self):
        self.cursor.execute("select eb.*,lo.location_firstname,lo.location_name from event_brief eb left join location lo on eb.event_location_id=lo.location_id")
    def selectPublicEvents(self):
        self.cursor.execute("select eb.*,lo.location_firstname,lo.location_name from event_brief eb left join location lo on eb.event_location_id=lo.location_id where eb.event_type=1")
    def selectById(self,attrs,id):
        self.cursor.execute("select "+ attrs +" from event_brief where event_id ="+str(id))
    def selectByIdsJoinLocation(self,ids):
        self.cursor.execute("select eb.*,lo.location_firstname,lo.location_name from event_brief eb left join location lo on eb.event_location_id=lo.location_id where event_id in (" + ids + ")")
    def selectByIds(self,attrs,ids):
        self.cursor.execute("select "+ attrs +" from event_brief where event_id in (" + ids + ")")
        
    def selectEUByUser(self,id):
        self.cursor.execute("select eu.eurelation_role,eu.eurelation_user_id,eb.* from eurelation eu left join event_brief eb on eu.eurelation_event_id=eb.event_id where eu.eurelation_user_id ="+str(id))
        
    def selectEUByUserIdRole(self,attrs,id,role):
        self.cursor.execute("select distinct "+ attrs +" from eurelation where eurelation_user_id ="+str(id)+' and eurelation_role="'+role)
    def selectEUByEventId(self,id,role):
        self.cursor.execute("select distinct eu.eurelation_user_id,u.user_name from eurelation eu left join user u on eu.eurelation_user_id=u.user_id where eu.eurelation_event_id ="+str(id)+' and eu.eurelation_role="'+str(role)+'"')
    def selectEUByUserId(self,attrs,id):
        self.cursor.execute("select distinct "+ attrs +" from eurelation where eurelation_user_id ="+str(id))
    def selectEU(self,eid,uid):
        self.cursor.execute("select distinct * from eurelation where eurelation_event_id="+str(eid)+" and eurelation_user_id="+str(uid))
    
    def insertEU(self,event_id,user_id,role):
        self.cursor.execute("insert into eurelation (eurelation_event_id,eurelation_user_id,eurelation_role) values(%s,%s,%s)",[event_id,user_id,role])
        self.conn.commit()
    def insertEvent(self,toinsert):
        self.cursor.execute("insert into event_brief " + toinsert)
        self.conn.commit()
    def insertEL(self,event_id,location_id,start_date,end_date,start_time,end_time):
        self.cursor.execute("insert into elrelation (elrelation_event_id,elrelation_location_id,elrelation_start_date,elrelation_end_date,elrelation_start_time,elrelation_end_time) values(%s,%s,%s,%s,%s,%s)",[event_id,location_id,start_date,end_date,start_time,end_time])
        self.conn.commit()
    # def delete(self,id):
    #     self.cursor.execute("delete from user where user_id=%s",id)
    #     self.conn.commit()
    def updateEvent(self,id,toset):
        self.cursor.execute("update event_brief set "+toset+" where event_id="+str(id))
        #self.cursor.execute("update user set (%s) where user_id=%s",(toset,id))
        self.conn.commit()
    def updateEventDetail(self,id,toset):
        self.cursor.execute("update event_detail set "+toset+" where event_id="+str(id))
        #self.cursor.execute("update user set (%s) where user_id=%s",(toset,id))
        self.conn.commit()
    def getLastEventId(self):
        self.cursor.execute("select examine_event_eid from examine_event order by examine_event_eid desc limit 1")

    def deleteELByEventId(self,eid):
        self.cursor.execute("delete from elrelation where elrelation_event_id=%s",eid)
        self.conn.commit()
    def deleteEventById(self,id):
        self.cursor.execute("delete from event_brief where event_id=%s",id)
        self.conn.commit()
    def deleteEUByEventId(self,event_id):
        self.cursor.execute("delete from eurelation where eurelation_event_id=%s and eurelation_role='creator'",event_id)
        self.conn.commit()
    def deleteEUByUserId(self,user_id):
        self.cursor.execute("delete from eurelation where eurelation_user_id=%s and eurelation_role='creator",user_id)
        self.conn.commit()
    def deleteEUByUserEvent(self,uid,eid):
        self.cursor.execute("delete from eurelation where eurelation_user_id=%s and eurelation_event_id=%s and eurelation_role='participant'",[uid,eid])
        self.conn.commit()
    def insertEventDetail(self,eid):
        self.cursor.execute("insert into event_detail (event_id,event_person_now) values(%s,0)",eid)
        self.conn.commit()
    def selectEventDetailById(self,eid):
        self.cursor.execute("select * from event_detail where event_id=%s",eid)


    def insertExamineEvent(self,eid,name,location_id,description,type,creator_id,start_date,end_date,start_time,end_time):
        sql="insert into examine_event \
            (examine_event_eid,examine_event_name,examine_event_location_id,examine_event_description,  \
            examine_event_type,examine_event_creator_id,examine_event_start_date,examine_event_end_date,examine_event_start_time,examine_event_end_time) \
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,[eid,name,location_id,description,type,creator_id,start_date,end_date,start_time,end_time])
        self.conn.commit()
    def selectAllExamineEvents(self):
        # self.cursor.execute("select eb.*,lo.location_firstname,lo.location_name from event_brief eb left join location lo on eb.event_location_id=lo.location_id")
        self.cursor.execute("select ee.*,lo.location_firstname,lo.location_name from examine_event ee left join location lo on ee.examine_event_location_id=lo.location_id")
    def selectExamineEventById(self,eid):
        self.cursor.execute("select ee.*,lo.location_firstname,lo.location_name from examine_event ee left join location lo on ee.examine_event_location_id=lo.location_id where ee.examine_event_eid=%s",eid)
    def deleteExamineEventById(self,eid):
        self.cursor.execute("delete from examine_event where examine_event_eid=%s",eid)
        self.conn.commit()

        
class LocationDB(DB):
    def __init__(self):
        super().__init__()
        
    def selectLocationById(self,attrs,id):
        self.cursor.execute("select "+ attrs +" from location where location_id ="+str(id))
    
    def selectAllLocations(self,attrs):
        self.cursor.execute("select "+attrs+" from location order by location_firstname,location_name")
        
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
    def selectLocationByFullName(self,attrs,firstname,name):
        self.cursor.execute("select "+attrs+' from location where location_firstname="'+str(firstname)+'" and location_name="'+str(name)+'"')
    