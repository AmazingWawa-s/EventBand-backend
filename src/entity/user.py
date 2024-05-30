import json
from entity.event import PrivateEvent,PublicEvent,Event
from entity.location import Location
from django.db import connection
import event_band.utils as utils

from entity.db import UserDB,EventDB,LocationDB
class User():
   
    def __init__(self,request):
        self.available=["id","name","password"]
        if type(request) is int:
            self.name=""
            self.id=request
            self.getFromDBById("*",self.id) 
            self.created_event_id=[i["eurelation_event_id"] for i in self.get_created_event_id()]
            self.participated_event_id=[i["eurelation_event_id"] for i in self.get_participated_event_id()]
        elif type(request) is str:
            self.name=request
            self.id=-1
            self.getFromDBByName("*",self.name)  
        else:
            # 默认初始化
            self.id=-1
            self.name=""
            self.password=""
            raise ValueError("class User initialize unexpected")
        
    
    
    def get(self,attr_list):
        return [getattr(self,attr) for attr in attr_list]

    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            if attr[5:] not in self.available:
                raise ValueError("Not available from User")
            elif attr[5:] in self.available:
                setattr(self,attr[5:],value)
        
    def getFromDBById(self,attrs,id):
        dbop=UserDB()
        dbop.selectById(attrs,id)
        result=dbop.get()
        if len(result)==1:
            self.set(result[0])
        else:raise ValueError("User Id Not Exist")
            
    def getFromDBByName(self,attrs,name):
        dbop=UserDB()
        dbop.selectByName(attrs,name)
        result=dbop.get()
        
        if len(result)==1:
            self.set(result[0])
        
        
   



    def autoUpdate(self):
        dbop=UserDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if value is not None and attr is not "id" and attr is not "available":
                sq+=('user_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]

        dbop.updateUser(self.id,sq)
            
        
    def __del__(self):
        pass

    def get_created_event_id(self):
        dbop=EventDB()
        dbop.selectEUByUserIdRole("event_id",self.id,1)
        return dbop.get()
    def get_participated_event_id(self):
        dbop=EventDB()
        dbop.selectEUByUserIdRole("event_id",self.id,0)
        return dbop.get()
        
    def create_private_event(self,dit:dict):
        
        edbop=EventDB()
        year=dit["start_date"]["year"]
        month=dit["start_date"]["month"]
        day=dit["start_date"]["day"]
        star_hour=dit["start_time"]["hour"]
        star_min=dit["start_time"]["minute"]
        star=star_hour*60+star_min
        en_hour=dit["end_time"]["hour"]
        en_min=dit["end_time"]["minute"]
        en=en_hour*60+en_min
        dt=str(year)+"-"+str(month)+"-"+str(day)
        edbop.checkCollision1(dt,star,en)
        result=edbop.get()
        if len(result)>=1:
            return False
        edbop.checkCollision2(dt,star,en)
        result=edbop.get()
        if len(result)>=1:
            return False
        edbop.checkCollision3(dt,star,en)
        result=edbop.get()
        if len(result)>=1:
            return False
        else :
            temp_event = PrivateEvent(-1)
            tid=utils.return_current_event_id(1)
            temp_event.set(self,{"event_id":tid,"event_name":dit["name"],"event_start":dt+":"+str(star),"event_end":dt+":"+str(en),"event_location":dit["location"],"event_description":dit["description"],"event_type":1,"event_creator_id":self.id})
            edbop.insertEU(temp_event.get(["id"])[0],self.id,1)
            edbop.insertEL(temp_event.get(["id"])[0],dit["location"],dt,star,en)
            return True
            
            
        
        
        
        
        

        

        

        
        return temp_event
    
    def create_public_event(self,event_dict:dict):
        temp_event = PublicEvent(-1,self.id)
        temp_event.set(self,event_dict)
    
        #更新活动简略表
        #sql_data = temp_event.get(["id","start_time","end_time","name","location","description","type"])
        #cursor.execute("insert into event_brief (event_id,event_start,event_end,event_name,event_location,event_description,event_type) values (%s,%s,%s,%s,%s,%s,%s)",sql_data)
        #更新活动详细信息表
        #sql_data=temp_event.get(["id","creator_id"])
        #cursor.execute("insert into eurelation (eurelation_event_id,eurelation_user_id,eurelation_role) values(%s,%s,1)",sql_data)
        #更新活动用户关系表
        #sql_data=temp_event.get(["id","creator_id"])
        #cursor.execute("insert into eurelation (eurelation_event_id,eurelation_user_id,eurelation_role) values(%s,%s,1)",sql_data)
        connection.commit()
        
        return temp_event  
    
    def delete_event(self,event_id):
        if event_id not in self.created_event_id:
            raise ValueError("Only creator can delete event")
        
        dbop=EventDB()
        dbop.deleteEUByEventId(event_id)

    def update_event(self):
        pass

    def get_all_locations(self):
        dbop=LocationDB()
        dbop.selectAllLocations()
        return dbop.get()



    


class SuperUser(User):
    def __init__(self,nid):
        
        super().__init__(nid)

    def __del__(self):
        if self.authority!=0:
            raise ValueError(f"expected authority=0,but ={self.authority}")   
        elif self.id>=0:
            self.autoUpdate()
        super().__del__()


    def broadcast(self):
        # 广播消息
        pass

    def check_event(self):
        # 活动审核
        pass
    
    def get_all_events(self,cursor):
        event_list=[]
        result = cursor.execute("select * from event")
        for i in result:
            temp_event = Event(-1)
            # 从数据库获取数据后，创建活动对象
            temp_event.set()
            event_list.append(temp_event)
        return event_list
    
    def add_location(self,location_dict):
        new_location=Location(location_dict,-1)

    def delete_location(self,location_id):
        dbop=LocationDB()
        dbop.deleteLocation(location_id)
    def update_location(self,location_dict,location_id):
        temp_location=Location(None,location_id)
        temp_location.set(location_dict)
    





class NormalUser(User):
    def __init__(self,nid):
        super().__init__(nid)

    def __del__(self):
        if self.id==-1:
            self.insertUser()
        elif self.id>=0:
            self.autoUpdate()
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

    def get_created_event(self):
        pass

    def get_participated_event(self):
        pass

    def sign_up_event(self):
        # 报名活动
        pass

    