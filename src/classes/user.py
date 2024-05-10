import json
import event_band.utils as utils

class User():
   
    def __init__(self,name=None,password=None,id=None):
        if isinstance(name,str):
            self.id = id
            self.name=name
            self.password=password
        elif password==None and id ==None and name!=None:
            data = json.loads(name.body.decode("utf-8"))
            self.id=-1
            self.name=data["userName"]
            self.password=utils.encoder(data["userPassword"])
        elif name is None and password is None and id is None:
            self.id=-1
            
            
        
    
   
        
    
    

    def __del__(self):
        pass
    
    def get(self,attrs):
        ls=[]
        for attr in attrs:
            if attr=="id":  ls.append(self.id)
            elif attr=="name": ls.append(self.name)
            elif attr=="password": ls.append(self.password)
        return ls

    def set(self,attrs,data):
        for i in range(len(attrs)):
            if attrs[i]=="id":  self.id=data[i]
            elif attrs[i]=="name": self.name=data[i]
            elif attrs[i]=="password": self.password=data[i]
   


class SuperUser(User):
    def __init__(self,id,name,password):
        super().__init__(id,name,password)
        self.auth = 0


class NormalUser(User):
    def __init__(self,id,name,password):
        super().__init__(id,name,password)
        self.auth = 1
