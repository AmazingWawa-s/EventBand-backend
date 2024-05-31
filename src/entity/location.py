from entity.db import LocationDB
class Location():
    def __init__(self,dict,id=-1):
        self.available=["id","name","description","capacity","type"]
        if id==-1:
            self.state="create"
            self.set(dict)
        else:
            self.state="update"
            self.getFromDB("*",self.id)
    
    def __del__(self):
        if self.state=="create":
            self.addlocation()
        elif self.state=="update":
            self.autoUpdate()
        
    def autoUpdate(self):
        dbop=LocationDB()
        dct=vars(self)
        sq=""
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('location_'+attr+'="'+str(value)+'", ')
        sq=sq[:-2]
        dbop.updateLocation(self.id,sq)

    def addLocation(self):
        dbop=LocationDB()
        dbop.insertNewLocation(self.name,self.description,self.capacity,self.type)     
        
        
    def get(self,attr_list):
        return [getattr(self,attr) for attr in attr_list]

    def set(self,attr_dict):
        print(1111)
        for attr,value in attr_dict.items():
            if attr[9:] not in self.available:
                raise ValueError("Not available from Location")
            elif attr[9:] in self.available:
                setattr(self,attr[9:],value)
                
    def getFromDB(self,attrs,id):
        dbop=LocationDB()
        dbop.selectLocationById(attrs,id)
        result=dbop.get()
        if len(result)==1:
            self.set(result[0])
        else:raise ValueError("Location Id Not Exist")
            
    #超级用户新增场地
    def addlocation(self):
        dbop=LocationDB()

        dbop.insertNewLocation(self.id,self.name,self.description,self.capacity,self.type)
    def deletelocation(self):
        dbop=LocationDB()
        dbop.deleteLocationById(self.id)
    
        
        
    