import pymysql

class DB():
    def __init__(self):
        self.conn=pymysql.connect(host="192.168.137.128",user="sa",password="",db="eventband",port=3306,charset="utf8")
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
    def checkExamineCollision(self,location,start_date,end_date,start_time,end_time):
        self.cursor.execute("select examine_event_id,examine_event_priority from examine_event where examine_event_location_id=%s and not examine_event_start_date>%s and not examine_event_end_date<%s and not examine_event_start_time>%s and not examine_event_end_time<%s",[location,end_date,start_date,end_time,start_time])
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
        self.cursor.execute("select eb."+ attrs +",u.user_name as event_creator_name,lo.location_firstname,lo.location_name from event_brief eb inner join user u on eb.event_creator_id=u.user_id  and eb.event_id="+str(id)+" left join location lo on lo.location_id=eb.event_location_id ")
    def selectByIdsJoinLocation(self,ids):
        self.cursor.execute("select eb.*,lo.location_firstname,lo.location_name from event_brief eb left join location lo on eb.event_location_id=lo.location_id where event_id in (" + ids + ")")
    def selectByIds(self,attrs,ids):
        self.cursor.execute("select "+ attrs +" from event_brief where event_id in (" + ids + ")")
        
    def selectEUByUser(self,id):
        self.cursor.execute("select eu.eurelation_role,eu.eurelation_user_id,eb.* from eurelation eu left join event_brief eb on eu.eurelation_event_id=eb.event_id where eu.eurelation_user_id ="+str(id))
        
    def selectEUByUserIdRole(self,attrs,id,role):
        self.cursor.execute("select distinct "+ attrs +" from eurelation where eurelation_user_id ="+str(id)+' and eurelation_role="'+role)
    def selectEUByEventId(self,id,role):
        self.cursor.execute("select distinct eu.eurelation_user_id,u.user_name,eu.eurelation_group_id from eurelation eu left join user u on eu.eurelation_user_id=u.user_id where eu.eurelation_event_id ="+str(id)+' and eu.eurelation_role="'+str(role)+'"')
    def selectEUByUserId(self,attrs,id):
        self.cursor.execute("select distinct "+ attrs +" from eurelation where eurelation_user_id ="+str(id))
    def selectEU(self,eid,uid):
        self.cursor.execute("select distinct * from eurelation where eurelation_event_id="+str(eid)+" and eurelation_user_id="+str(uid))
    def selectEidFromEUByUid(self,uid):
        self.cursor.execute("select distinct eurelation_event_id from eurelation where eurelation_user_id="+str(uid))
    
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
    def updateEUGroup(self,groupid,eid,uid):
        self.cursor.execute('update eurelation set eurelation_group_id='+str(groupid)+' where eurelation_event_id='+str(eid)+" and eurelation_user_id="+str(uid))
        self.conn.commit()
    def getLastEventId(self):
        self.cursor.execute("select event_id from event_brief order by event_id desc limit 1")

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


    def insertExamineEvent(self,name,location_id,description,type,creator_id,start_date,end_date,start_time,end_time,event_priority):
        sql="insert into examine_event \
            (examine_event_name,examine_event_location_id,examine_event_description,  \
            examine_event_type,examine_event_creator_id,examine_event_start_date,examine_event_end_date,examine_event_start_time,examine_event_end_time,examine_event_priority) \
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,[name,location_id,description,type,creator_id,start_date,end_date,start_time,end_time,event_priority])
        self.conn.commit()
    def selectAllExamineEvents(self):
        self.cursor.execute("select ee.*,lo.location_firstname,lo.location_name from examine_event ee left join location lo on ee.examine_event_location_id=lo.location_id")
    def selectExamineEventById(self,eid):
        self.cursor.execute("select ee.*,lo.location_firstname,lo.location_name from examine_event ee left join location lo on ee.examine_event_location_id=lo.location_id where ee.examine_event_id=%s",eid)
    def deleteExamineEventById(self,eid):
        self.cursor.execute("delete from examine_event where examine_event_id=%s",eid)
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
        self.conn.commit()
    def getLastLocationId(self):
        self.cursor.execute("select location_id from location order by location_id desc limit 1")
    def deleteLocationById(self,id):
        self.cursor.execute("delete from location where location_id=%s",id)
        self.cursor.execute("delete from elrelation where elrelation_location_id=%s",id)
        self.conn.commit()
    def selectLocationByFullName(self,attrs,firstname,name):
        self.cursor.execute("select "+attrs+' from location where location_firstname="'+str(firstname)+'" and location_name="'+str(name)+'"')

class GroupDB(DB):
    def __init__(self):
        super().__init__()
    def insertGroupDB(self,toinsert):
        self.cursor.execute("insert into `groups` " + toinsert)
        self.conn.commit()
    def getLastGroupId(self):
        self.cursor.execute("select group_id from `groups` order by group_id desc limit 1")
    def selectGroupById(self,attrs,gid):
        self.cursor.execute("select "+attrs+" from `groups` where group_id="+str(gid))
    def selectEventGroups(self,eid):
        self.cursor.execute("select * from `groups` where group_event_id="+str(eid))
    

class MessageDB(DB):
    def __init__(self):
        super().__init__()
    def insertMessageDB(self,toinsert):
        self.cursor.execute("insert into message " + toinsert)
        self.conn.commit()
    def selectMessageByUserId(self,attrs,uid):
        self.cursor.execute("select "+attrs+" from message where message_user_id="+str(uid)+" order by message_id desc")

class ChatMessageDB(DB):
    def __init__(self):
        super().__init__()
    def insertMessageDB(self,toinsert):
        self.cursor.execute("insert into chatrecord " + toinsert)
        self.conn.commit()
    def selectGroupMessagesByEId(self,attrs,eid):
        self.cursor.execute("select "+attrs+" from chatrecord where chr_type=0 and chr_event_id="+str(eid))
    def selectPrivateMessagesByUids(self,attrs,my_id,your_id):
        self.cursor.execute("select "+attrs+" from chatrecord where chr_type=1 \
                            and ( \
                            (chr_sender_id="+str(my_id)+" and chr_recv_id="+str(your_id)+") \
                            or (chr_sender_id="+str(your_id)+" and chr_recv_id="+str(my_id)+") \
                            ) order by chr_time" )
    def selectAllMessages(self,uid,eids):
        sql_old = """
            SELECT
                IF(chr_type = 0, chr_event_id, chr_recv_id) AS title,
                chr_type,
                chr_time,
                chr_sender_id,
                chr_content
            FROM
                chatrecord
            WHERE
                chr_sender_id = %s OR (chr_type = 1 AND chr_recv_id = %s)
            ORDER BY
                chr_type, title, chr_time;
        """
        sql="""
            SELECT
                c.chr_type,
                c.chr_time,
                u.user_name AS chr_sender_name,
                c.chr_sender_id,
                c.chr_content,
                IF(c.chr_type = 0, c.chr_event_id, c.chr_recv_id) AS title_id,
                IF(c.chr_type = 0, e.event_name, u2.user_name) AS title
            FROM
                chatrecord c
            LEFT JOIN
                event_brief e ON c.chr_event_id = e.event_id
            LEFT JOIN
                user u ON c.chr_sender_id = u.user_id
            LEFT JOIN
                user u2 ON c.chr_recv_id = u2.user_id
            WHERE
                c.chr_sender_id = %s OR (c.chr_type = 1 AND c.chr_recv_id = %s) OR (c.chr_type = 0 AND c.chr_event_id in (""" \
            + eids \
            +"""
                    ))
            ORDER BY
                c.chr_type, title, c.chr_time;
        """
        self.cursor.execute(sql, [uid, uid])   
         
class CommentDB(DB):
    def __init__(self):
        super().__init__()
    def insertCommentDB(self,toinsert):
        self.cursor.execute("insert into comment " + toinsert)
        self.conn.commit()
    def selectCommentByEventId(self,attrs,eid):
        self.cursor.execute("select "+attrs+" from comment where comment_event_id="+str(eid)+" order by comment_time desc")
    
class CostremarkDB(DB):
    def __init__(self):
        super().__init__()     
    def selectAllRemarksByEid(self,eid):
        self.cursor.execute("select cr.*,u.user_name as cr_user_name from cost_remark cr inner join user u on cr.cr_user_id=u.user_id where cr_event_id="+str(eid))
    def insertRemark(self,toinsert):
        self.cursor.execute("insert into cost_remark " + toinsert)
        self.conn.commit()
    def updateRemark(self,id,toset):
        self.cursor.execute("update cost_remark set "+toset+" where cr_id="+str(id))
        self.conn.commit()
    def selectRemarksById(self,attrs,id):
        self.cursor.execute("select "+attrs+" from cost_remark where cr_id="+str(id))


class ResourceDB(DB):
    def __init__(self):
        super().__init__()   
    def insertResourceDB(self,toinsert):
        self.cursor.execute("insert into resource " + toinsert)
        self.conn.commit()
    def getLastResourceId(self):
        self.cursor.execute("select resource_id from resource order by resource_id desc limit 1")
    def selectResourceById(self,attrs,rid):
        self.cursor.execute("select "+attrs+" from resource where resource_id="+str(rid))
    def updateResource(self,id,toset):
        self.cursor.execute("update resource set "+toset+" where resource_id="+str(id))
        self.conn.commit()
    def deleteResourceById(self,rid):
        self.cursor.execute("delete from resource where resource_id=%s",rid)
        self.conn.commit()
    def selectEventResources(self,eid):
        self.cursor.execute("select * from resource where resource_eid="+str(eid))

class SubeventDB(DB):
    def __init__(self):
        super().__init__()      
    def insertSubevent(self,toinsert):
        self.cursor.execute("insert into event_sub " + toinsert)
        self.conn.commit()
    def selectSubeventByEid(self,attrs,eid):
        self.cursor.execute("select "+attrs+" from event_sub where event_sub_eid="+str(eid))