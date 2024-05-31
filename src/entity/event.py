from entity.db import UserDB,EventDB

class Event():
    def __init__(self,event_id):

        self.id = event_id
        self.creator_id=-1
        self.name = ""
        self.start_time=0
        self.end_time=0
        self.start_date:str=""
        self.end_date:str=""
        self.location = -1
        self.description=""
        self.participants:list = []
        self.type=""

        self.available=["id","creator_id","name","start","end","location","description","type"]


        if event_id == -1:
            # 创建
            self.state="create"
        elif event_id>=0:
            # 活动已经创建过，直接载入数据
            self.state="update"
            self.getFromDB("*")
            
            
    def __del__(self):
        if self.state=="create":
            # 新建
            self.insertEvent()
        elif self.state=="update":
            # 更新
            self.autoUpdate()

    
    def get(self,attr_list):
        return [getattr(self,attr) for attr in attr_list]
    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            setattr(self,attr[6:],value)

    def getFromDB(self,attrs:str):
        dbop=EventDB()
        dbop.selectById(attrs,self.id)
        result=dbop.get()        
        if len(result)==1:
            self.set(result[0])
        # 获取参加者id
        dbop.selectEUByEventId("user_id",self.id)
        result=dbop.get()
        for i in result:
            participant_id=i["user_id"]
            self.participants.append(participant_id)

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
        dbop.insertEvent(self.id,sq)



    def autoUpdate(self):
        dbop=EventDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('event_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]
        dbop.updateEvent(self.id,sq)

        # 数据库应该根据 创建者/参与者 区分查询
        # for i in self.participants:
        #     dbop.insertEU(self.id, i, 0)






class PrivateEvent(Event):
    def __init__(self,event_id):
        super().__init__(self,event_id)
        self.type="private"

    def to_dict(self) -> dict:
        # 前端接口
        temp_dict = {
            "eventName":self.name,
        }
        return temp_dict

 
class PublicEvent(Event):
    def __init__(self,id):
        super().__init__(self,id)
        self.type="public"
 