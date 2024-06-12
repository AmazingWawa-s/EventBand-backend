from entity.db import CostremarkDB
from entity.event import PrivateEvent
import event_band.utils as utils
class Costremark():
#初始化函数---------------------------------------------------
    def __init__(self,id,state):
        if id!=-1:
            self.id=id
        self.state=state
        self.available=["id","event_id","user_id","reason","cost","time","passed","remark"]#允许与数据库交互的属性
        if self.state=="select":
            pass
        elif self.state=="update":
            self.getEventIdFromDB()
        elif id==-1 and self.state=="create":
            self.passed="undo"
        else :raise ValueError("unexpected initialize class Costremark")
            
#析构函数-------------------------------------------------------        
    def __del__(self):
        if self.state=="create":
            # 新建
            self.insertRemark()
        elif self.state=="update":
            # 更新 
            temp_event=PrivateEvent(self.event_id,"join")
            if self.passed=="true":
                temp_event.add_cost(self.cost)
            self.updateRemark()

        elif self.state=="select":
            pass
        else :raise ValueError("unexpected delete class Costremark in function __del__")

#从类中获得属性-------------------------------------------------------   
    def get(self,attr_list):
        if utils.Exist(self,attr_list):
            return [getattr(self,attr) for attr in attr_list]
        else:raise ValueError("class Costremark lack attributes in function get")

#给类中的属性赋值-------------------------------------------------------   
    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            setattr(self,attr[3:],value)

#向Costremark库中增加信息-------------------------------------------------------   
    def insertRemark(self):
        dbop=CostremarkDB()
        dct=vars(self)
        sq="("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('cr_'+attr+', ')
        sq=sq[:-2]
        sq+=") values ("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('"'+str(value)+'", ')
        sq=sq[:-2]  
        sq+=")"
        dbop.insertRemark(sq)

#更新event数据库中关于此活动的信息-------------------------------------------------------   
    def updateRemark(self):
        dbop=CostremarkDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('cr_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]
        dbop.updateRemark(self.id,sq)

    @staticmethod
    def getAllRemarks(eid):
        dbop=CostremarkDB()
        dbop.selectAllRemarksByEid(eid)
        result=dbop.get()
        return result
    
    def getEventIdFromDB(self):
        dbop=CostremarkDB()
        dbop.selectRemarksById("cr_event_id,cr_cost",self.id)
        result=dbop.get()
        if len(result)>0:
            self.set({"cr_event_id":result[0]["cr_event_id"],"cr_cost":result[0]["cr_cost"]})