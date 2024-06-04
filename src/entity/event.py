from entity.db import UserDB,EventDB

class Event():
#初始化函数---------------------------------------------------
    def __init__(self,event_id,state):
        self.state=state#活动的状态
        self.id = event_id
        # self.creator_id=-1
        # self.name = ""
        # self.start_time=0
        # self.end_time=0
        # self.start_date:str=""
        # self.end_date:str=""
        # self.location_id = -1
        # self.description=""
        # self.participants:list = []#参与到这个活动的人
        self.type=-1
        self.available=["id","creator_id","name","start","end","location_id","description","type"]#允许与数据库交互的属性
   
        if self.id>=0 and self.state=="select":
            self.getFromDB("*")
        elif self.state=="update":
            pass
        elif self.id==-1 and self.state=="create":
            pass
        else :raise ValueError("unexpected initialize event")
            
#析构函数-------------------------------------------------------        
    def __del__(self):
        if self.state=="create":
            # 新建
            self.insertEvent()
        elif self.state=="update":
            # 更新
            self.updateEvent()
        elif self.state=="select":
            pass
        else :raise ValueError("unexpected delete event")

#从类中获得属性-------------------------------------------------------   
    def get(self,attr_list):
        return [getattr(self,attr) for attr in attr_list]

#给类中的属性赋值-------------------------------------------------------   
    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            setattr(self,attr[6:],value)

#从event库中获得关于此活动的内容-------------------------------------------------------   
    def getFromDB(self,attrs:str):
        dbop=EventDB()
        dbop.selectById(attrs,self.id)
        result=dbop.get()        
        if len(result)==1:
            self.set(result[0])
        else :raise ValueError("Event getFromDB Error")
    
#从eurelation库中获得参加此活动的人-------------------------------------------------------   
    def getFromEUDB(self):
        # 获取参加者id
        dbop=EventDB()
        dbop.selectEUByEventId("eurelation_user_id",self.id)
        result=dbop.get()
        for i in result:
            participant_id=i["eurelation_user_id"]
            self.participants.append(participant_id)

#向event库中增加此活动的信息-------------------------------------------------------   
    def insertEvent(self):
        dbop=EventDB()
        dct=vars(self)
        sq="("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('event_'+attr+', ')
        sq=sq[:-2]
        sq+=") values ("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('"'+str(value)+'", ')
        sq=sq[:-2]  
        sq+=")"
        dbop.insertEvent(sq)

#更新event数据库中关于此活动的信息-------------------------------------------------------   
    def updateEvent(self):
        dbop=EventDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('event_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]
        dbop.updateEvent(self.id,sq)

       



#将此活动的与数据库有关的属性变成字典-------------------------------------------------------   
    def to_dict(self) -> dict:
        # 前端接口
        result_dict = {}
        for key,value in vars(self).items():
            if key in self.available:
                result_dict[key]=value
        return result_dict





class PrivateEvent(Event):
    def __init__(self,event_id):
        super().__init__(event_id)
        self.type=0     # 私有

    def to_dict(self) -> dict:
        # 前端接口
        temp_dict = {
            "eventName":self.name,
        }
        return temp_dict

 
 
 
class PublicEvent(Event):
    def __init__(self,id):
        super().__init__(id)
        self.type=1    # 公有
 