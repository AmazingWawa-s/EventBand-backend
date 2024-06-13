import hashlib
import jwt
import json
from event_band.settings import SECRET_KEY
import time
from django.db import connection
from django.http import JsonResponse
from entity.user import User
from entity.semaphore import Semaphore
from entity.db import EventDB,LocationDB,GroupDB,ResourceDB
import random
import string

All_conn_dict={}

current_event_id=0
current_location_id=0
current_group_id=0
current_resource_id=0
event_id_sema=Semaphore(1)
location_id_sema=Semaphore(1)
group_id_sema=Semaphore(1)
resource_id_sema=Semaphore(1)
def Encoder(raw):
    md5 = hashlib.md5()
    md5.update(str(raw).encode("utf-8"))
    return md5.hexdigest()

def Generate_token(payload):
    try:
        token=jwt.encode(payload,SECRET_KEY,algorithm="HS256")
        return token
    except Exception as e:
        return "generateTokenError:"+str(e)
    
#初始化current_event_id   
def Count_event():
    global current_event_id
    global event_id_sema
    try:
        dbop=EventDB()
        dbop.getLastEventId()
        result=dbop.get()
        event_id_sema=Semaphore(1)
        
        if len(result)>0:
            current_event_id=result[0]["examine_event_eid"]+1
            
        else: 
            current_event_id=1
    except Exception as e:
        return JsonResponse({"code":0,"msg":"countEventError:"+str(e)})
def Return_current_event_id(num):
    global current_event_id
    global event_id_sema
    event_id_sema.P()
    temp=current_event_id
    current_event_id=current_event_id+num
    event_id_sema.V()
    return temp
#初始化current_location_id
def Count_location():
    global current_location_id
    global location_id_sema
    try:
        dbop=LocationDB()
        dbop.getLastLocationId()
        result=dbop.get()
        location_id_sema=Semaphore(1)
        if len(result)>0:
            current_location_id=result[0]["location_id"]+1
        else: 
            current_location_id=1
    except Exception as e: 
        return JsonResponse({"code":0,"msg":"countEventError:"+str(e)})
def Return_current_location_id(num):
    global current_location_id
    global location_id_sema
    location_id_sema.P()
    temp=current_location_id
    current_location_id=current_location_id+num
    location_id_sema.V()
    return temp

def Count_group():
    global current_group_id
    global group_id_sema
    try:
        dbop=GroupDB()
        dbop.getLastGroupId()
        result=dbop.get()
        group_id_sema=Semaphore(1)
        if len(result)>0:
            current_group_id=result[0]["group_id"]+1
        else: 
            current_group_id=1
    except Exception as e: 
        return JsonResponse({"code":0,"msg":"countGroupError:"+str(e)})
def Return_current_group_id(num):
    global current_group_id
    global group_id_sema
    group_id_sema.P()
    temp=current_group_id
    current_group_id=current_group_id+num
    group_id_sema.V()
    return temp

def Count_resource():
    global current_resource_id
    global resource_id_sema
    try:
        dbop=ResourceDB()
        dbop.getLastResourceId()
        result=dbop.get()
        resource_id_sema=Semaphore(1)
        if len(result)>0:
            current_resource_id=result[0]["resource_id"]+1
        else: 
            current_resource_id=1
    except Exception as e: 
        return JsonResponse({"code":0,"msg":"countResourceError:"+str(e)})
def Return_current_resource_id(num):
    global current_resource_id
    global resource_id_sema
    resource_id_sema.P()
    temp=current_resource_id
    current_resource_id=current_resource_id+num
    resource_id_sema.V()
    return temp
    
def checkEventCreator(eid):
        dbop=EventDB()
        dbop.selectById("event_creator_id",eid)
        res=dbop.get()
        if len(res)==0:
            raise ValueError("Event doesn't exist")
        elif len(res)==1:
            return res[0]["event_creator_id"]
        else:raise ValueError("Error in fun checkEventCreator")
import string
import random

m={"A":12,"B":4,"C":2,"D":19,"E":25,"F":1}
option=["A","B","C","D"]
weight=[167,607,41,233,73,449,197,401,521,1979,1999,641,101,157,61,71,211,7]
def Generate_invite_id(id,length=10):
    a=random.choice(option)
    prefix = hex(id+m[a])[2:]+a
    length = length - len(prefix)
    chars=string.ascii_letters+string.digits
    result=prefix + ''.join([random.choice(chars) for i in range(length)])
    
    result=result[::-1]
    
    result=Valid(result)+result[3:]
    return result

def Get_id(code):
    if Valid(code)!=code[0:3]:
        return -1
    ori=code[::-1]
    temp=""
    for i in code:
        if i.isupper():
            temp=i
    a=ori.split(temp)[0]
    return int(a, 16)-m[temp]
def Valid(strin):
    num=0
    for i in range(3,len(strin)):
        num=num+ord(strin[i])*weight[i]
    a=num%26
    b=(num%10)%26
    c=num%10
    
    return chr(65+a)+chr(97+b)+chr(48+c)


s_set = string.ascii_letters + string.digits
raw_code_len = 8

tid=20
res=Generate_invite_id(tid,10)


#检查类的实例中是否存在ls中的所有属性-------------------------------------------
def Exist(clas,ls):
    for i in ls:
        if not hasattr(clas,i):
            return False
    return True


def Cal_priority(user_priority,location_capacity,person_num,time_span,days):
    result = user_priority * location_capacity / person_num / time_span / days * 100
    return result


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_user(user_id, message_content:dict):
    message_content["userId"]=user_id
    message = json.dumps(message_content)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'message': message,
        }
    )

