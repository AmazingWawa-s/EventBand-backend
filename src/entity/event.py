from entity.user import User

class Event():
    def __init__(self,creator_id):
        self.creator_id=creator_id
        self.id = -1
        self.name = ""
        self.start_time:str= ""
        self.end_time:str= ""
        self.location=""
        self.description=""
        self.participants:list = []
        self.type=""
    
    def get(self,attr_list):
        if len(attr_list)==1:
            return getattr(self,attr_list[0])
        return [getattr(self,attr) for attr in attr_list]
    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            setattr(self,attr,value)


class PrivateEvent(Event):
    def __init__(self,id,name,start_time,end_time):
        super().__init__(self,id,name,start_time,end_time)
        self.type="private"

    def update_event(self):
        pass

    def to_dict(self) -> dict:
        # 前端接口
        temp_dict = {
            "name":self.name
        }
        return temp_dict

 
class PublicEvent(Event):
    def __init__(self,id,name,start_time,end_time):
        super().__init__(self,id,name,start_time,end_time)
        self.type="public"
 