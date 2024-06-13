import event_band.utils as utils
from entity.db import ResourceDB,EventDB
class Resource():
    def __init__(self,id,state):
        self.id=id
        self.state=state
        self.available=["eid","name","num","condition","id"]
        if self.id==-1 and self.state=="create":
            pass
        elif self.state=="update" and self.id>=0:
            self.getFromDB("*")
        elif self.state=="select" and self.id>=0:
            self.getFromDB("*")
        elif self.state=="delete" and self.id>=0:
            pass
        else :raise ValueError("class Resource initilize unexpected")
            
    def __del__(self):
        if self.state=="create":
            self.insertGroup()
        elif self.state=="update" and self.id>=0:
            pass
        elif self.state=="select":
            pass
        elif self.state=="delete":
            self.deleteResource()
        else :raise ValueError("class Resource delete unexpected")
    
    
    #从类中获得属性-------------------------------------------------------   
    def get(self,attr_list):
        if utils.Exist(self,attr_list):
            return [getattr(self,attr) for attr in attr_list]
        else:raise ValueError("class Resource lack attributes in function get")

    #给类中的属性赋值-------------------------------------------------------   
    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            setattr(self,attr[9:],value)
    
    
    #向event库中增加此活动的信息-------------------------------------------------------   
    def insertGroup(self):
        dbop=ResourceDB()
        dct=vars(self)
        sq="("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('resource_'+attr+', ')
        sq=sq[:-2]
        sq+=") values ("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('"'+str(value)+'", ')
        sq=sq[:-2]  
        sq+=")"
        dbop.insertResourceDB(sq)
    
    def getFromDB(self,attrs:str):
        dbop=ResourceDB()
        dbop.selectResourceById(attrs,self.id)
        result=dbop.get()       
        if len(result)==1:
            self.set(result[0])
        elif len(result)==0:
            raise ValueError("Resource doesn't exist")
        else :raise ValueError("Resource getFromDB Error")
    
    def updateResource(self):
        dbop=ResourceDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('resource_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]
        dbop.updateResource(self.id,sq)
    def deleteResource(self):
        dbop=ResourceDB()
        dbop.deleteResourceById(self.id)
        
    