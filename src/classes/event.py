from user import User
from typing import Optional

class Event():
    def __init__(self,id,name,start_time,end_time,creator: User,description=""):
        self.id = id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.description=description
        self.creator=creator
        self.participants = []



class PrivateEvent(Event):
    def __init__(self,id,name,start_time,end_time):
        super().__init__(self,id,name,start_time,end_time)
        self.type="private"
 
class PublicEvent(Event):
    def __init__(self,id,name,start_time,end_time):
        super().__init__(self,id,name,start_time,end_time)
        self.type="public"
 