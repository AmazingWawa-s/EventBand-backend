import json
import event_band.utils as utils

class User():
   
    def __init__(self,request=None):
        if request is not None:
            data = json.loads(request.body.decode("utf-8"))
            self.id=-1
            self.name=data["userName"]
            self.password=utils.encoder(data["userPassword"])
        else:
            self.id=-1
            self.name=""
            self.password=""

    def __del__(self):
        pass
    
    def get(self,attr_list):
        return [getattr(self,attr) for attr in attr_list]

    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            setattr(self,attr,value)

   


class SuperUser(User):
    def __init__(self,id,name,password):
        super().__init__(id,name,password)
        self.auth = 0


class NormalUser(User):
    def __init__(self,id,name,password):
        super().__init__(id,name,password)
        self.auth = 1
