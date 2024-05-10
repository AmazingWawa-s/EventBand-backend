import hashlib
import jwt
from event_band.settings import SECRET_KEY
import time
from django.db import connection
from django.http import JsonResponse
current_event_id=0

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
        return str(e)
    
    
def count_event():
    cursor=connection.cursor()
    try:
        cursor.execute("select event_id from event order by event_id desc limit 1")
        result=cursor.fetchall()
        if len(result)>0:
            current_event_id=result[0][0]+1
            
        else: 
            current_event_id=1
    except Exception as e:
        return JsonResponse({"code":0,"msg":"countEventError:"+str(e)})
def return_event_id():
    return current_event_id

def add_event_id(num):
    global current_event_id
    current_event_id=current_event_id+num
        
def template1(request):

    try:
        data = json.loads(request.body.decode("utf-8"))
        cd,potential_id=utils.validtoken(data["userToken"])   
        if cd==1:
            pass
        elif cd==2:
            return JsonResponse({"code":1,"msg":potential_id})
        elif cd==0:
            return JsonResponse({"code":0,"msg":potential_id})
    except Exception as e:
        connection.rollback()
        return JsonResponse({"code":0,"msg":""+str(e)})

