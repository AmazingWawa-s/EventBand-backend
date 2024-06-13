from entity.db import MessageDB,ChatMessageDB
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
    
class ChatMessage(Message):
    def __init__(self,sender_id,content,type,time):
        self.sender_id=sender_id
        self.content=content
        self.type=type
        self.time=time
        self.available=["time","sender_id","recv_id","type","content","event_id"]
    def __del__(self):
        self.insertMessage()

    def set(self,attr_dict):
        for attr,value in attr_dict.items():
            setattr(self,attr[4:],value)

    def insertMessage(self):
        dbop=ChatMessageDB()
        dct=vars(self)
        sq="("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('chr_'+attr+', ')
        sq=sq[:-2]
        sq+=") values ("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('"'+str(value)+'", ')
        sq=sq[:-2]  
        sq+=")"
        dbop.insertMessageDB(sq)
    @staticmethod
    def getGroupMessagesByEid(eid):
        dbop=ChatMessageDB()
        dbop.selectGroupMessagesByEId("*",eid)
        return dbop.get()
    @staticmethod
    def getPrivateMessageByUids(my_id,your_id):
        dbop=ChatMessageDB()
        dbop.selectPrivateMessagesByUids("*",my_id,your_id)
        return dbop.get()            