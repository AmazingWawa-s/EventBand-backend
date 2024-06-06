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
def encoder(raw):
    md5 = hashlib.md5()
    md5.update(str(raw).encode("utf-8"))
    return md5.hexdigest()
def validtoken(tok):
    try:   
        decode_token=jwt.decode(tok,SECRET_KEY,algorithms="HS256")
        exp_time=int(decode_token["my_exp"])
        if time.time() >exp_time:
            return 2,"token out of date"
        else :
            return 1,decode_token["userId"]
    except Exception as e:
        return 0,"validTokenError:"+str(e)
def generatetoken(payload):
    try:
        token=jwt.encode(payload,SECRET_KEY,algorithm="HS256")
        return token
    except Exception as e:
        return "generateTokenError:"+str(e)
    
#初始化current_event_id   
def count_event():
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
def return_current_event_id(num):
    global current_event_id
    global event_id_sema
    event_id_sema.P()
    temp=current_event_id
    current_event_id=current_event_id+num
    event_id_sema.V()
    return temp
#初始化current_location_id
def count_location():
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
def return_current_location_id(num):
    global current_location_id
    global location_id_sema
    location_id_sema.P()
    temp=current_location_id
    current_location_id=current_location_id+num
    location_id_sema.V()
    return temp
    
    
    


        
    # def template1(request):
        
    #     try:
    #         data = json.loads(request.body.decode("utf-8"))
    #         cd,potential_id=utils.validtoken(data["userToken"])   
    #         if cd==1:
    #             pass
    #         elif cd==2:
    #             return JsonResponse({"code":1,"msg":potential_id})
    #         elif cd==0:
    #             return JsonResponse({"code":0,"msg":potential_id})
    #     except Exception as e:
    #         connection.rollback()
    #         return JsonResponse({"code":0,"msg":""+str(e)})

# def createUser(result):
#     ls=[]
#     for i in result:
#         tempUser = User(result[i][0],result[i][1])
#         ls.append(tempUser)

#     return ls
def is_json(r):
    try:
        json.loads(r)
        return True
    except Exception as e:
        return False
    
import string
import random

m={"A":12,"B":4,"C":2,"D":19,"E":25,"F":1}
option=["A","B","C","D"]
weight=[167,607,41,233,73,449,197,401,521,1979,1999,641,101,157,61,71,211,7]
def generate_invite_id(id,length=10):
    a=random.choice(option)
    prefix = hex(id+m[a])[2:]+a
    length = length - len(prefix)
    chars=string.ascii_letters+string.digits
    result=prefix + ''.join([random.choice(chars) for i in range(length)])
    
    result=result[::-1]
    
    result=valid(result)+result[3:]
    return result

def get_id(code):
    if valid(code)!=code[0:3]:
        return -1
    ori=code[::-1]
    temp=""
    for i in code:
        if i.isupper():
            temp=i
    a=ori.split(temp)[0]
    return int(a, 16)-m[temp]
def valid(strin):
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
res=generate_invite_id(tid,10)
print(res)

print(get_id(res))


#检查类的实例中是否存在ls中的所有属性-------------------------------------------
def exist(clas,ls):
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