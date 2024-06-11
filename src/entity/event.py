from entity.db import UserDB,EventDB
import event_band.utils as utils
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
        self.detail_available=["person_now","budget","reim_id","signup_time","person_max"]
        if self.id>=0 and self.state=="select":
            self.getFromDB("*")
            self.participants:list = []
            self.par_id:list=[]
            self.getFromEUDB()
            self.detail={}
            self.getFromEventDetail()
        elif self.state=="join":
            self.detail={}
            self.getFromEventDetail()
        elif self.state=="update":
            pass
        elif self.id==-1 and self.state=="create":
            pass
        else :raise ValueError("unexpected initialize class Event")
            
#析构函数-------------------------------------------------------        
    def __del__(self):
        if self.state=="create":
            # 新建
            self.insertEvent()
        elif self.state=="update":
            # 更新
            self.updateEvent()
            self.updateEventDetail()
        elif self.state=="select":
            pass
        elif self.state=="join":
            self.updateEventDetail()
        else :raise ValueError("unexpected delete class Event in function __del__")

#从类中获得属性-------------------------------------------------------   
    def get(self,attr_list):
        if utils.exist(self,attr_list):
            return [getattr(self,attr) for attr in attr_list]
        else:raise ValueError("class Event lack attributes in function get")

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
        elif len(result)==0:
            raise ValueError("EventId Not Exist")
        else :raise ValueError("Event getFromDB Error")
    
#从eurelation库中获得参加此活动的人-------------------------------------------------------   
    def getFromEUDB(self):
        # 获取参加者id
        dbop=EventDB()
        dbop.selectEUByEventId(self.id,"participant")
        result=dbop.get()
        if utils.exist(self,["participants"]):
            self.participants=result
            for i in result:
                self.par_id.append(i["eurelation_user_id"])
        else:raise ValueError("class Event lack attributes in function getFromEUDB")
    def getFromEventDetail(self):
        dbop=EventDB()
        dbop.selectEventDetailById(self.id)
        result=dbop.get()
        
        if len(result)==1:
            self.detail=result[0]
            self.set(result[0])
        elif len(result)==0:
            raise ValueError("EventId Not Exist")
        else :raise ValueError("Event getFromDB Error")
        

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

    def updateEventDetail(self):
        dbop=EventDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if attr in self.detail_available:
                sq+=('event_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]
        dbop.updateEventDetail(self.id,sq)


    def joinEvent(self,event_id,user_id):

        if self.person_now>=self.person_max:
            return 2

        dbop=EventDB()
        dbop.selectEU(event_id,user_id)
        res=dbop.get()
        if len(res)>0:
            return 0

        dbop.insertEU(event_id,user_id,"participant")
        self.person_now=self.person_now+1
        return 1
    
    @staticmethod
    def deleteParticipant(uid,eid):
        dbop=EventDB()
        dbop.deleteEUByUserEvent(uid,eid)
        temp_event=PrivateEvent(eid,"join")
        temp_event.person_now=temp_event.person_now-1



#将此活动的与数据库有关的属性变成字典-------------------------------------------------------   
    def toDict(self) -> dict:
        # 前端接口
        result_dict = {}
        for key,value in vars(self).items():
            if key in self.available:
                result_dict[key]=value
        return result_dict
    
        



class PrivateEvent(Event):
    def __init__(self,event_id,state):
        super().__init__(event_id,state)
        self.type=0     # 私有

 

class PublicEvent(Event):
    def __init__(self,id,state):
        super().__init__(id,state)
        self.type=1    # 公有
 