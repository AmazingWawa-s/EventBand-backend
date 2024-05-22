import json
from entity.event import PrivateEvent,PublicEvent,Event
from django.db import connection

from entity.db import UserDB
class User():
   
    def __init__(self,request):
        if type(request) is int:
            self.name=""
            self.id=request
            self.getFromDBById("*",self.id) 
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
        if len(attr_list)==1:
            return getattr(self,attr_list[0])
        return [getattr(self,attr) for attr in attr_list]

    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            
            setattr(self,attr[5:],value)
        
    def getFromDBById(self,attrs,id):
        dbop=UserDB()
        dbop.select(attrs,id)
        result=dbop.get()
        if len(result)!=0:
            self.set(result[0])
    def getFromDBByName(self,attrs,name):
        dbop=UserDB()
        dbop.select(attrs,name)
        result=dbop.get()
        
        if len(result)!=0:
            self.set(result[0])
        
   

    def deleteUser(self):
        dbop=UserDB()
        dbop.delete(self.id)
    def insertUser(self):
        dbop=UserDB()
        dbop.insertNewUser(self.name,self.password)
    def autoSave(self):
        dbop=UserDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if value is not None and attr is not "id":
                sq+=('user_'+attr+'="'+value+'", ')
        sq=sq[:-2]
        
        

        dbop.update(self.id,sq)
            
        
    def __del__(self):

        if self.id==-1:
            self.insertUser()
        elif self.id>=0:
            self.autoSave()
            
            
            
            
        
        
        
        
    def create_private_event(self,cursor,event_dict:dict):
        temp_event = PrivateEvent(self.id)
        temp_event.set(self,event_dict)
    
        #更新活动简略表
        sql_data = temp_event.get(["id","start_time","end_time","name","location","description","type"])
        cursor.execute("insert into event_brief (event_id,event_start,event_end,event_name,event_location,event_description,event_type) values (%s,%s,%s,%s,%s,%s,%s)",sql_data)
        #更新活动用户关系表
        sql_data=temp_event.get(["id","creator_id"])
        cursor.execute("insert into eurelation (eurelation_event_id,eurelation_user_id,eurelation_role) values(%s,%s,1)",sql_data)
        connection.commit()
        
        return temp_event

    def create_public_event(self,cursor,event_dict:dict):
        temp_event = PublicEvent(self.id)
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
    

    


class SuperUser(User):
    def __init__(self,id,name,password):
        super().__init__(id,name,password)
        self.auth = 0

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





class NormalUser(User):
    def __init__(self,id,name,password):
        super().__init__(id,name,password)
        self.auth = 1

    def get_created_event(self):
        pass

    def get_participated_event(self):
        pass

    def sign_up_event(self):
        # 报名活动
        pass
    
    