from entity.db import MessageDB
class Message():
    def __init__(self,uid,content,type,link,detail):
        self.user_id=uid
        self.content=content
        self.type=type
        self.link=link
        self.detail=detail
        self.available=["time","user_id","content","type","link","detail"]
    def __del__(self):
        self.insertMessage()
        pass
    def insertMessage(self):
        dbop=MessageDB()
        dct=vars(self)
        sq="("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('message_'+attr+', ')
        sq=sq[:-2]
        sq+=") values ("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('"'+str(value)+'", ')
        sq=sq[:-2]  
        sq+=")"
        dbop.insertMessageDB(sq)
    @staticmethod
    def getUserMessage(uid):
        dbop=MessageDB()
        dbop.selectMessageByUserId("*",uid)
        return dbop.get()