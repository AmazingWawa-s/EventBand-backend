from entity.db import SubeventDB

class Subevent():
    def __init__(self,eid,time,title,content,participants):
        self.eid=eid
        self.time=time
        self.title=title
        self.content=content
        self.participants=participants

        self.available=["eid","time","title","content","participants"]
    def __del__(self):

        self.insertSubevent()


    def insertSubevent(self):
        dbop=SubeventDB()
        dct=vars(self)
        sq="("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('event_sub_'+attr+', ')
        sq=sq[:-2]
        sq+=") values ("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('"'+str(value)+'", ')
        sq=sq[:-2]  
        sq+=")"
        dbop.insertSubevent(sq)
    
    @staticmethod
    def getSubevent(eid):
        dbop=SubeventDB()
        dbop.selectSubeventByEid("*",eid)
        return dbop.get()
