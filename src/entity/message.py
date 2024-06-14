from entity.db import MessageDB,ChatMessageDB,EventDB
import datetime
from asgiref.sync import async_to_sync
from event_band.global_vars import All_conn_dict

class Message():
    def __init__(self,uid,content,type,link,detail):
        self.user_id=uid
        self.content=content
        self.type=type
        self.link=link
        self.detail=detail
        self.available=["time","user_id","content","type","link","detail"]
    def __del__(self):
        self.time=datetime.datetime.now()

        self.insertMessage()
        temp_dict=self.toDict()

        origin_time = datetime.datetime.strptime(str(self.time), "%Y-%m-%d %H:%M:%S.%f")
        temp_dict["message_time"] = origin_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        global All_conn_dict
        if self.user_id in All_conn_dict:
            async_to_sync(All_conn_dict[self.user_id].send_notification)(temp_dict,None)

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
    
    def toDict(self) -> dict:
        # 前端接口
        result_dict = {}
        for key,value in vars(self).items():
            if key in self.available:
                result_dict["message_"+key]=value
        return result_dict
    

    
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

    @staticmethod
    def getAllMessages(uid):
        dbop=EventDB()
        dbop.selectEidFromEUByUid(uid)
        result=dbop.get()

        eidlist=[]
        if len(result)>0:
            eidlist=[str(result[i]["eurelation_event_id"]) for i in range(len(result))]
        eids = ",".join(eidlist)

        dbop=ChatMessageDB()
        dbop.selectAllMessages(uid,eids)
        result=dbop.get()


        grouped_chats = {}
        for row in result:
            title = row['title']
            chr_type = row['chr_type']
            chat_entry = {
                'chr_time': row['chr_time'],
                'chr_sender': row['chr_sender_name'],
                'chr_sender_id': row['chr_sender_id'],
                'chr_content': row['chr_content']
            }

            if title not in grouped_chats:
                grouped_chats[title] = {
                    'title': title,
                    'title_id': row['title_id'],
                    'chr_type': chr_type,
                    'chatlist': []
                }
            grouped_chats[title]['chatlist'].append(chat_entry)

        final_output = list(grouped_chats.values())   
        return final_output      