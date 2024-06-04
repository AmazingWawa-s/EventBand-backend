import json
from entity.event import PrivateEvent,PublicEvent,Event
from entity.location import Location
from django.db import connection
import event_band.utils as utils

from entity.db import UserDB,EventDB,LocationDB
class User():
#初始化函数---------------------------------
    def __init__(self,request):
        self.available=["id","name","password","authority"]#允许被保存到数据库中的属性
        if type(request) is int:
            self.name=""
            self.id=request
            self.getFromDBById("*",self.id)
            self.created_event_id=[i["event_id"] for i in self.get_created_event()]#该用户创建的活动
            self.participated_event_id=[i["event_id"] for i in self.get_participated_event()]#该用户参加的活动
        elif type(request) is str:
            self.name=request
            self.id=-1
            self.password=""
            self.getFromDBByName("*",self.name)  
        else:
            # 默认初始化
            self.id=-1
            self.name=""
            self.password=""
            raise ValueError("class User initialize unexpected")
        
#析构函数-----------------------------------      
    def __del__(self):
        pass
        
    
    
    def get(self,attr_list):
        return [getattr(self,attr) for attr in attr_list]

    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            if attr[5:] in self.available:
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
            if attr in self.available:
                sq+=('user_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]

        dbop.updateUser(self.id,sq)
            
    def get_created_event(self):
        dbop=EventDB()
        dbop.selectEUByUserIdRole("eurelation_event_id",self.id,1)
        event_ids=dbop.get()
        if len(event_ids)==0:
            return []

        ids=""
        for i in event_ids:
            ids+='"'
            ids+=str(i["eurelation_event_id"])
            ids+='", '
        ids=ids[:-2]
        dbop.selectByIds("*",ids)
        result=dbop.get()
        for i in result:
            pass
        return result
    
    def get_participated_event(self):
        dbop=EventDB()
        dbop.selectEUByUserIdRole("eurelation_event_id",self.id,0)
        event_ids=dbop.get()
        if len(event_ids)==0:
            return []

        ids=""
        for i in event_ids:
            ids+='"'
            ids+=str(i["eurelation_event_id"])
            ids+='", '
        ids=ids[:-2]

        dbop.selectByIds("*",ids)
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
        edbop.checkCollision1(dit["location_id"],dt,star,en)
        result=edbop.get()
        if len(result)>=1:
            return False
        edbop.checkCollision2(dit["location_id"],dt,star,en)
        result=edbop.get()
        if len(result)>=1:
            return False
        edbop.checkCollision3(dit["location_id"],dt,star,en)
        result=edbop.get()
        if len(result)>=1:
            return False
        else :
            temp_event = PrivateEvent(-1,"create")
            tid=utils.return_current_event_id(1)
            temp_event.set({"event_id":tid,"event_name":dit["name"],"event_start":dt+":"+str(star),"event_end":dt+":"+str(en),"event_location_id":dit["location_id"],"event_description":dit["description"],"event_type":1,"event_creator_id":self.id})
            edbop.insertEU(temp_event.get(["id"])[0],self.id,1)
            edbop.insertEL(temp_event.get(["id"])[0],dit["location_id"],dt,star,en)
            return True
            
            
        
        
        
        
        

        

        

        
        
    
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
        dbop=EventDB()
        dbop.selectById("*",event_id)
        result=dbop.get()

        if len(result)==0:
            raise ValueError("Event Id not exist")
        if event_id not in self.created_event_id:
            raise ValueError("Only creator can delete event")
        
        
        dbop.deleteEUByEventId(event_id)
        dbop.deleteEventById(event_id)

    def update_event(self):
        pass

    def get_all_locations_id(self):
        dbop=LocationDB()
        dbop.selectAllLocations("location_id")
        return dbop.get()
        

    def get_all_locations(self):
        ids=self.get_all_locations_id()
        location_list=[Location(None,i["location_id"]) for i in ids]
            # 处理结果
        result = []
        current_firstname = None
        current_list = []
        
        for location in location_list:
            firstname, name, capacity, id,description = location.get(["firstname","name","capacity","id","description"])
            
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
        
        return result
    


    


class SuperUser(User):
    def __init__(self,nid):
        super().__init__(nid)
        if "authority" not in vars(self).keys():
            raise ValueError("expected authority")
        
        if self.authority != 0:
            raise ValueError("not superuser")



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
    
    def get_all_events(self):
        dbop=EventDB()
        dbop.selectAll("event_id")
        ids=dbop.get()
        return [Event(i["event_id"],"select") for i in ids]
    
    def add_location(self,location_dict):
        new_location=Location(location_dict,-1)
        
        new_location.set({"location_id":utils.return_current_location_id(1)})

    def delete_location(self,location_id):
        dbop=LocationDB()
        dbop.deleteLocationById(location_id)
    def update_location(self,location_dict,location_id):
        temp_location=Location(None,location_id)
        temp_location.set(location_dict)
    





class NormalUser(User):
    def __init__(self,nid):
        super().__init__(nid)

    def __del__(self):
        if self.id==-1 and self.password!="":
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

    def get_all_normal_users(self):
        pass


    def sign_up_event(self):
        # 报名活动
        pass

    