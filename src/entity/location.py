from entity.db import LocationDB
import event_band.utils as utils

class Location():
#初始化函数---------------------------------------------------
    def __init__(self,id,state):
        self.available=["id","firstname","name","description","capacity","type"]#允许与数据库交互的属性
        self.state=state#实例的状态
        self.id=id
        if id==-1 and self.state=="create":
            pass 
        elif id>=0 and self.state=="update":
            pass
        elif id>=0 and self.state=="select":
            self.getFromDB("*",self.id)
        else :raise ValueError("unexpected initialize class Location")
        
#析构函数-------------------------------------------------------    
    def __del__(self):
        if self.state=="create":
            self.addLocation()
        elif self.state=="update":
            self.updateLocation()
        elif self.state=="select":
            pass
        else:raise ValueError("unexpected delete class Location in function __del__")
      
#更新event数据库中关于此活动的信息-------------------------------------------------------   
    def updateLocation(self):
        dbop=LocationDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('location_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]
        dbop.updateLocation(self.id,sq)
        
#从类中获得属性-------------------------------------------------------         
    def get(self,attr_list):
        if utils.exist(self,attr_list):
            return [getattr(self,attr) for attr in attr_list]
        else:raise ValueError("class Location lack attributes in function get")
    
#给类中的属性赋值-------------------------------------------------------   
    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            setattr(self,attr[9:],value)
           
#从location库中获得关于此活动的内容-----------------------------------------
    def getFromDB(self,attrs,id):
        dbop=LocationDB()
        dbop.selectLocationById(attrs,id)
        result=dbop.get()
        if len(result)==1:
            self.set(result[0])
        elif len(result)==0:
            pass
        else:raise ValueError("Location getFromDB Error")
            
#超级用户新增场地----------------------------------------------------------
    def addLocation(self):
        dbop=LocationDB()
        if utils.exist(self,["firstname","name","description","capacity","type"]):
            dbop.insertNewLocation(self.id,self.firstname,self.name,self.description,self.capacity,self.type)
        else:raise ValueError("class Location lack attributes in function addlocation")


#将此地点的与数据库有关的属性变成字典------------------------------------------
    def toDict(self) -> dict:
        # 前端接口
        result_dict = {}
        for key,value in vars(self).items():
            if key in self.available:
                result_dict[key]=value
        return result_dict
    


    