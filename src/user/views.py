from django.shortcuts import render
import json
from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
from event_band.settings import EXPIRE_TIME
import time
from entity.user import SuperUser,NormalUser

#注册
def register(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        tUser = NormalUser(data["userName"])
        
        # 用户名已存在
        if tUser.get(["id"])[0]>=0:
            return JsonResponse({"code":1,"userNameExist":True})
        
        # 用户名不存在时创建新的用户
        encode_password=utils.encoder(data["userPassword"])
        tUser.set({"user_password":encode_password,"user_authority":1})
        #tUser.insertUser()
        return JsonResponse({"code":1,"userNameExist":False,"register_ok":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"registerError:"+str(e)})

#登录
def login(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        tUser = NormalUser(data["userName"])
        
        # 输入的用户名不存在时返回错误
        if tUser.get(["id"])[0]==-1:
            return JsonResponse({"code":1,"userNameExist":False})
        
        # 用户名存在
        encode_password=utils.encoder(data["userPassword"])
        
        # 密码正确
        if tUser.get(["password"])[0] == encode_password:
            payload={
                "userId":tUser.get(["id"])[0],
                "my_exp":int(time.time())+EXPIRE_TIME
            }
            Token=utils.generatetoken(payload)
            #tUser.updateToDB()
            return JsonResponse({"code":1,"userNameExist":True,"userPasswordOk":True,"userToken":Token})
        # 密码错误
        else:
            return JsonResponse({"code":1,"userNameExist":True,"userPasswordOk":False})     
    except Exception as e:
        return JsonResponse({"code":0,"msg":"loginError:"+str(e)})
 
#注销用户
def remove(request):
    try:
        id = request.userid
        tUser=NormalUser(id)
        tUser.deleteUser()
        return JsonResponse({"code":1,"removeOk":True})    
    except Exception as e:
        return JsonResponse({"code":0,"msg":"removeError:"+str(e)})   
    
    
#改变密码
def change_pwd(request):
    

    try:
        data = json.loads(request.body.decode("utf-8"))
        new_password = utils.encoder(data["userNewPassword"])
        
        id = request.userid
        tUser=NormalUser(id)
        if new_password == tUser.get(["password"])[0]:
        # 新密码和原密码相同
            return JsonResponse({"code":1,"duplicatePassword":True})
        else :
            tUser.changePassword(new_password)   
        return JsonResponse({"code":1,"duplicatePassword":False,"updatePassword":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"changePwdError:"+str(e)})

def super_login(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        if "userAuthority" not in data:
            raise ValueError("no authority error")
        sUser = SuperUser(data["userName"])
        if data["userAuthority"] !=0 or sUser.get(["authority"])[0]!=0:
            return JsonResponse({"code":1,"isSuperUser":False}) 
        
        
        # 输入的用户名不存在时返回错误
        if sUser.get(["id"])[0]==-1:
            return JsonResponse({"code":1,"isSuperUser":True,"userNameExist":False})
        
        # 用户名存在
        encode_password=utils.encoder(data["userPassword"])
        
        # 密码正确
        if sUser.get(["password"])[0] == encode_password:
            payload={
                "userId":sUser.get(["id"])[0],
                "my_exp":int(time.time())+EXPIRE_TIME
            }
            Token=utils.generatetoken(payload)
            #tUser.updateToDB()
            return JsonResponse({"code":1,"isSuperUser":True,"userNameExist":True,"userPasswordOk":True,"userToken":Token})
        # 密码错误
        else:
            return JsonResponse({"code":1,"isSuperUser":True,"userNameExist":True,"userPasswordOk":False})     
    except Exception as e:
        return JsonResponse({"code":0,"msg":"superLoginError:"+str(e)})