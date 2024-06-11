import hashlib
import jwt
import json
from event_band.settings import SECRET_KEY
import time
from django.db import connection
from django.http import JsonResponse
from entity.user import User
from entity.semaphore import Semaphore
from entity.db import EventDB,LocationDB
import random
import string


current_event_id=0
event_id_sema=Semaphore(1)

current_location_id=0
location_id_sema=Semaphore(1)
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
            current_event_id=result[0]["event_id"]+1
            
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
# if __name__=="__main__":
#     for i in range(10,500,35):
#         code = generate_invite_id(i)
#         id_hex = code.split('L')[0]
#         id  = get_id(id_hex)
#         print(code,id)