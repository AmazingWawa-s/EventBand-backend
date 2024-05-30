from entity.db import LocationDB
class Location():
    def __init__(self,name,capacity,description,type,id=-1):
        self.available=["id","name","description","capacity","type"]
        if id<0:
            raise ValueError("Location Id <0")
        else:
            self.id=id
            self.name = name
            self.description=description
            self.capacity = capacity
            self.type=type
            self.getFromDB("*",self.id)
    def __del__(self):
        self.autoUpdate()
        pass
    def autoUpdate(self):
        dbop=LocationDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if value is not None and attr is not "id" and attr is not "available":
                sq+=('location_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]
        
        

        dbop.updateLocation(self.id,sq)
        
        
        
    def get(self,attr_list):
        return [getattr(self,attr) for attr in attr_list]

    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            if attr[9:] not in self.available:
                raise ValueError("Not available from Location")
            elif attr[9:0] in self.available:
                setattr(self,attr[9:],value)
    def getFromDB(self,attrs,id):
        dbop=LocationDB()
        dbop.selectById(attrs,id)
        result=dbop.get()
        if len(result)==1:
            self.set(result[0])
        else:raise ValueError("Location Id Not Exist")
            

        
        
    