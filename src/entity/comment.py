from entity.db import CommentDB
class Comment():
    def __init__(self,uid,content,eid,time):
        self.user_id=uid
        self.content=content
        self.event_id=eid
        self.time=time
        self.available=["time","user_id","content","event_id"]
    def __del__(self):
        self.insertComment()
    def insertComment(self):
        dbop=CommentDB()
        dct=vars(self)
        sq="("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('comment_'+attr+', ')
        sq=sq[:-2]
        sq+=") values ("
        for attr,value in dct.items():
            if attr in self.available:
                sq+=('"'+str(value)+'", ')
        sq=sq[:-2]  
        sq+=")"
        dbop.insertCommentDB(sq)
    @staticmethod
    def getComments(eid):
        dbop=CommentDB()
        dbop.selectCommentByEventId("*",eid)
        return dbop.get()