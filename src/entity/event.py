from entity.db import UserDB,EventDB

class Event():
    def __init__(self,event_id):
        self.id = event_id
        self.creator_id=-1
        self.name = ""
        self.start_time:str= ""
        self.end_time:str= ""
        self.start_date:str=""
        self.end_date:str=""
        self.location = -1
        self.description=""
        self.participants:list = []
        self.type=""

        if self.id != -1:
            # 活动已经创建过，直接载入数据
            self.getFromDB("*")


    
    def get(self,attr_list):
        if len(attr_list)==1:
            return getattr(self,attr_list[0])
        return [getattr(self,attr) for attr in attr_list]
    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            setattr(self,attr[6:],value)

    def getFromDB(self,attrs:str):
        dbop=EventDB()
        dbop.selectById(attrs,self.id)
        result=dbop.get()        
        if len(result)!=0:
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
            if (value is not None) and (attr is not "id") and (attr is not "participants"):
                sq+=('event_'+attr+', ')
        sq=sq[:-2]
        sq+=") values ("
        for attr,value in dct.items():
            if (value is not None) and (attr is not "id") and (attr is not "participants"):
                sq+=('"'+str(value)+'", ')
        sq=sq[:-2]  
        sq+=")"
        dbop.insert(self.id,sq)

        for i in self.participants:
            dbop.insertEU(self.id, i, 0)



    def autoSave(self):
        dbop=EventDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if (value is not None) and (attr is not "id") and (attr is not "participants"):
                sq+=('event_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]
        dbop.update(self.id,sq)

        for i in self.participants:
            dbop.insertEU(self.id, i, 0)

    def __del__(self):
        if :
            return

        dbop=EventDB()
        dbop.selectById("event_id",self.id)
        result = dbop.get()
        if len(result)==0:
            # 新建
            self.insertEvent()
        elif len(result)>0:
            # 更新
            self.autoSave()




class PrivateEvent(Event):
    def __init__(self,event_id,creator_id):
        super().__init__(self,event_id,creator_id)
        self.type="private"

    def to_dict(self) -> dict:
        # 前端接口
        temp_dict = {
            "eventName":self.name,
        }
        return temp_dict

 
class PublicEvent(Event):
    def __init__(self,id,name,start_time,end_time):
        super().__init__(self,id,name,start_time,end_time)
        self.type="public"
 