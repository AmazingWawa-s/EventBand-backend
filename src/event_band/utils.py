import hashlib
import jwt
from event_band.settings import SECRET_KEY
import time
from django.db import connection

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
        connection.rollback()
        return 0,"validTokenError:"+str(e)
def generatetoken(payload):
    try:
        token=jwt.encode(payload,SECRET_KEY,algorithms="HS256")
        return token
    except Exception as e:
        pass
def template1(request):

    try:
        data = json.loads(request.body.decode("utf-8"))
        cd,potential_id=utils.validtoken(data["userToken"])   
        if cd==1:
            
        elif cd==2:
            return JsonResponse({"code":1,"msg":potential_id})
        elif cd==0:
            return JsonResponse({"code":0,"msg":potential_id})
    except Exception as e:
        connection.rollback()
        return JsonResponse({"code":0,"msg":""+str(e)})

