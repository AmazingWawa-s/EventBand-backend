import event_band.utils as utils
from entity.db import GroupDB,EventDB
class Group():
    def __init__(self,id,state):
        self.state=state
        self.id=id
        self.available=["id","name","event_id"]
        if self.state=="create" and self.id==-1:
            pass
        elif self.state=="select":
            self.name=""
            self.getFromDB("*")
        else:raise ValueError("class Group initilize unexpected")
        
    def __del__(self):
        if self.state=="create":
            self.insertGroup()
        elif self.state=="select":
            pass
        else :raise ValueError("class Group delete unexpected")
        pass
    #从类中获得属性-------------------------------------------------------   
    def get(self,attr_list):
        if utils.Exist(self,attr_list):
            return [getattr(self,attr) for attr in attr_list]
        else:raise ValueError("class Group lack attributes in function get")

    #给类中的属性赋值-------------------------------------------------------   
    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            setattr(self,attr[6:],value)
    #向event库中增加此活动的信息-------------------------------------------------------   
    def insertGroup(self):
        dbop=GroupDB()
        dct=vars(self)
        sq="("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('group_'+attr+', ')
        sq=sq[:-2]
        sq+=") values ("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('"'+str(value)+'", ')
        sq=sq[:-2]  
        sq+=")"
        dbop.insertGroupDB(sq)
    
    def getFromDB(self,attrs:str):
        dbop=GroupDB()
        dbop.selectGroupById(attrs,self.id)
        result=dbop.get()       
        if len(result)==1:
            self.set(result[0])
        elif len(result)==0:
            raise ValueError("Group doesn't exist")
        else :raise ValueError("Group getFromDB Error")
    def joinGroup(self,eid,uid):
        dbop=EventDB()
        dbop.updateEUGroup(self.name,eid,uid)
        
        
            
    