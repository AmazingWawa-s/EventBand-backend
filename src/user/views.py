from django.shortcuts import render
import json
from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
from event_band.settings import EXPIRE_TIME
import time
from entity.user import SuperUser,NormalUser,User

#注册
def register(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        tUser = NormalUser(data["userName"],"create")
        # 用户名已存在
        if tUser.get(["id"])[0]>=0:
            return JsonResponse({"code":1,"userNameExist":True})
        
        # 用户名不存在时创建新的用户
        encode_password=utils.encoder(data["userPassword"])
        tUser.set({"user_password":encode_password,"user_authority":1})
       
        return JsonResponse({"code":1,"userNameExist":False,"register_ok":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"registerError:"+str(e)})

#登录
def login(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        tUser = NormalUser(data["userName"],"login")
        
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
        tUser=NormalUser(id,"delete")
        return JsonResponse({"code":1,"removeOk":True})    
    except Exception as e:
        return JsonResponse({"code":0,"msg":"removeError:"+str(e)})   
    
    
#改变密码
def change_pwd(request):
    

    try:
        data = json.loads(request.body.decode("utf-8"))
        new_password = utils.encoder(data["userNewPassword"])
        
        id = request.userid

        tUser=NormalUser(id,"update")

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
        sUser = SuperUser(data["userName"],"login")
        
        # 输入的用户名不存在时返回错误
        if sUser.get(["id"])[0]==-1:
            return JsonResponse({"code":1,"isSuperUser":False,"userNameExist":False})
        
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
    

def get_all_locations(request):
    try:
        result,tempmap=User.getAllLocations()
        return JsonResponse({"code":1,"data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getAllLocationsError:"+str(e)})

def add_location(request):
    try:
        user = SuperUser(request.userid,"classattrs")
        data = json.loads(request.body.decode("utf-8"))
        location_dict={
            "location_firstname":data["locationFirstname"],
            "location_name":data["locationName"],
            "location_description":data["locationDescription"],
            "location_capacity":data["locationCapacity"],
            "location_type":data["locationType"],
        }
        result=user.add_location(location_dict)
        if result is False:
            return JsonResponse({"code":1,"NameDuplicated":True,"addLocationOk":False})
        
        return JsonResponse({"code":1,"addLocationOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"addLocationError:"+str(e)})

def delete_location(request):
    try:
        user = SuperUser(request.userid,"classattrs")
        data = json.loads(request.body.decode("utf-8"))
        user.delete_location(data["locationId"])
        return JsonResponse({"code":1,"removeOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"deleteLocationError:"+str(e)})