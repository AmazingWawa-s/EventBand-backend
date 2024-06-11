import json
from entity.event import PrivateEvent,PublicEvent,Event
from entity.location import Location
from django.db import connection
import event_band.utils as utils

from entity.db import UserDB,EventDB,LocationDB
class User():
#初始化函数---------------------------------
    def __init__(self,nid,state):
        self.available=["id","name","password","authority"]#允许被保存到数据库中的属性
        self.state=state
        if type(nid) is int and self.state=="classattrs":#调用用户包含的类，而不对用户本身的属性修改
            self.id=nid
            self.getFromDBById("user_authority",self.id)
        elif type(nid) is int and self.state=="delete":#删除用户
            self.id=nid
            self.authority=-1
            self.created_event_id=[]
            self.participated_event_id=[]
            self.getFromDBById("user_authority",self.id)
            self.getRelatedEvents()
        elif type(nid) is int and self.state=="update":#更新用户
            self.id=nid
            self.getFromDBById("user_authority,user_password",self.id)
        elif type(nid) is int and self.state=="select":#查询数据
            self.id=nid
            self.getFromDBById("*",self.id)
            self.events=self.getEventsFromDB()
            self.locations,self.locationmap=User.getAllLocations()
            self.matchEventLocation()
        elif type(nid) is str and self.state=="create":#创建用户
            self.name=nid
            self.password=""
            self.id=-1
            self.authority=1
            self.getFromDBByName("user_id,user_authority",self.name)
        elif type(nid) is str and self.state=="login":#用户登录
            self.name=nid
            self.id=-1
            self.getFromDBByName("user_id,user_password,user_authority",self.name)    
        else:
            raise ValueError("class User initialize unexpected")
        
#析构函数-----------------------------------      
    def __del__(self):
        pass
        
    
#从类中获得属性-------------------------------------------------------   
    def get(self,attr_list):
        if utils.Exist(self,attr_list):
            return [getattr(self,attr) for attr in attr_list]
        else:raise ValueError("class User lack attributes in function get")
        
#给类中的属性赋值-------------------------------------------------------   
    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            if attr[5:] in self.available:
                setattr(self,attr[5:],value)

#通过id获取用户信息-----------------------------------------------------
    def getFromDBById(self,attrs,id):
        dbop=UserDB()
        dbop.selectById(attrs,id)
        result=dbop.get()
        if len(result)==1:
            self.set(result[0])
        elif len(result)==0:
            pass
        else:raise ValueError("class User error in function getFromDBById ")
        
#通过name获取用户信息--------------------------------------------------- 
    def getFromDBByName(self,attrs,name):
        dbop=UserDB()
        dbop.selectByName(attrs,name)
        result=dbop.get()
        if len(result)==1 :
            self.set(result[0])
        elif len(result)==0:
            pass
        else:raise ValueError("class User error in function getFromDBByName ")
        
#更新用户信息----------------------------------------------------------
    def updateUser(self):
        dbop=UserDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('user_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]
        dbop.updateUser(self.id,sq)
            
#获取与用户有关的活动-----------------------------------------------------
    def getEvents(self):
        return self.events
    def getLocations(self):
        return self.locations
    
    def getRelatedEvents(self):
        dbop=EventDB()
        dbop.selectEUByUser(self.id)
        result=dbop.get()

        for i in result:
            if i["eurelation_role"]=="creator":
                self.created_event_id.append(i["event_id"])
            elif i["eurelation_role"]=="participant":
                self.participated_event_id.append(i["event_id"])
        
    
    def getEventsFromDB(self):
        dbop=EventDB()
        dbop.selectEUByUser(self.id)
        result=dbop.get()
        
        return result
    
    @staticmethod
    def createPrivateEvent(uid,dit:dict):
        
        edbop=EventDB()
        year,month,day=dit["start_date"]["year"],dit["start_date"]["month"],dit["start_date"]["day"]
        start_hour,start_min=dit["start_time"]["hour"],dit["start_time"]["minute"]
        startnum=start_hour*60+start_min
        end_hour,end_min=dit["end_time"]["hour"],dit["end_time"]["minute"]
        endnum=end_hour*60+end_min
        
        datestr=str(year)+"-"+str(month)+"-"+str(day)
        
        for location in dit["location_id"]:
            flag=1
            edbop.checkCollision1(location,datestr,startnum,endnum)
            result=edbop.get()
            if len(result)>=1:
                flag=0
            
            edbop.checkCollision2(location,datestr,startnum,endnum)
            result=edbop.get()
            if len(result)>=1:
                flag=0
            
            edbop.checkCollision3(location,datestr,startnum,endnum)
            result=edbop.get()
            if len(result)>=1:
                flag=0
        
            if flag==1:
                temp_event = PrivateEvent(-1,"create")
                eid=utils.Return_current_event_id(1)
                temp_event.set({"event_id":eid,"event_name":dit["name"],"event_start":datestr+":"+str(startnum),"event_end":datestr+":"+str(endnum),"event_location_id":location,"event_description":dit["description"],"event_type":dit["type"],"event_creator_id":uid})
                edbop.insertEU(eid,uid,"creator")
                edbop.insertEL(eid,location,datestr,startnum,endnum)
                edbop.insertEventDetail(eid)
                return 1,eid
        return 0,-1
            
    def matchEventLocation(self):
        for event in self.events:
            event["event_location_name"]=self.locationmap[event["event_location_id"]]
        
        
        
    @staticmethod    
    def getPublicEvents():
        dbop=EventDB()
        dbop.selectPublicEvents()
        return dbop.get()

    
    def deleteEvent(self,event_id):
        dbop=EventDB()
        if event_id not in self.created_event_id:
            raise ValueError("Only creator can delete event")
        
        dbop.deleteELByEventId(event_id)
        dbop.deleteEUByEventId(event_id)
        dbop.deleteEventById(event_id)

    
    @staticmethod
    def getAllLocations():
        dbop=LocationDB()
        dbop.selectAllLocations("*")
        dbresult=dbop.get()
        result = []
        locationmap={}
        current_firstname = None
        current_list = []
        for i in dbresult:
            firstname=i["location_firstname"]
            name=i["location_name"]
            capacity=i["location_capacity"]
            id=i["location_id"]
            description=i["location_description"]
            locationmap[id]=firstname+name
            if firstname != current_firstname:
                if current_firstname is not None:
                    result.append({
                        "firstname": current_firstname,
                        "list": current_list
                    })
                current_firstname = firstname
                current_list = []
            
            current_list.append({
                "name": name,
                "size": capacity,
                "id": id,
                "description":description
            })
        
        # 最后一个一级地点
        if current_firstname is not None:
            result.append({
                "firstname": current_firstname,
                "list": current_list
            })
        
        return result,locationmap
        

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#类分界线 
#----------------------------------------------------------------------------------------------------------------------------------------------------------- 

class SuperUser(User):
    def __init__(self,nid,state):
        super().__init__(nid,state)
        if "authority" not in vars(self).keys():
            raise ValueError("expect authority")
        
        if self.authority != 0:
            raise ValueError("not superuser")



    def __del__(self):
        if self.authority!=0:
            raise ValueError(f"expected authority=0,but ={self.authority}")   
        elif self.id>=0 and self.state=="update":
            self.updateUser()
        elif self.id>=0 and self.state=="classattrs":
            pass
        elif self.state=="login":
            pass
        else:raise ValueError("unexpected delete class SuperUser in function __del__")
        super().__del__()


    def broadcast(self):
        # 广播消息
        pass

    def checkEvent(self):
        # 活动审核
        pass
    
    def getAllEvents(self):
        dbop=EventDB()
        dbop.selectAllEvents()
        return dbop.get()
    
    def addLocation(self,location_dict) -> bool:
        dbop=LocationDB()
        dbop.selectLocationByFullName("location_id",location_dict["location_firstname"],location_dict["location_name"])
        if len(dbop.get())>0:
            return False
        new_location=Location(-1,"create")
        new_location.set(location_dict)
        new_location.set({"location_id":utils.Return_current_location_id(1)})
        return True
        
#超级用户删除场地----------------------------------------------------------
    def deleteLocation(self,location_id):
        dbop=LocationDB()
        dbop.deleteLocationById(location_id)
        
    def updateLocation(self,location_dict,location_id):
        temp_location=Location(location_id,"update")
        temp_location.set(location_dict)
    


#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#类分界线 
#----------------------------------------------------------------------------------------------------------------------------------------------------------- 


class NormalUser(User):
    def __init__(self,nid,state):
        super().__init__(nid,state)

    def __del__(self):
        if self.id>=0 and self.state=="select":
            pass
        elif self.state=="login":
            pass
        elif self.state=="create":
            if self.id==-1:
                self.insertUser()
        elif self.id>=0 and self.state=="update":
            self.updateUser()
        elif self.id>=0 and self.state=="delete":
            self.deleteUser()
        elif self.id>=0 and self.state=="classattrs":
            pass
        else:raise ValueError("unexpected delete class NormalUser in function __del__")
        super().__del__()
        

    def deleteUser(self):
        if self.authority==0:
            raise ValueError("superuser can't be deleted")
        dbop=UserDB()
        dbop.deleteUser(self.id)
    def changePassword(self,newPassword):
        if self.authority==0:
            raise ValueError("superuser can't change password")
        self.password=newPassword
        
    def insertUser(self):
        if self.authority==0:
            raise ValueError("superuser can't be added")
        dbop=UserDB()
        dbop.insertNewUser(self.name,self.password)


    def signupEvent(self):
        # 报名活动
        pass

    