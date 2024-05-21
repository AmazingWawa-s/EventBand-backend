from django.shortcuts import render
import json
from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
from event_band.settings import EXPIRE_TIME
import time
from entity.user import User

#注册
def register(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        tUser = User(data["userName"])
        
        # 用户名已存在
        if tUser.get(["id"])>=0:
            return JsonResponse({"code":1,"userNameExist":True})
        
        # 用户名不存在时创建新的用户
        encode_password=utils.encoder(data["userPassword"])
        tUser.set({"user_password":encode_password})
        return JsonResponse({"code":1,"userNameExist":False,"register_ok":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"registerError:"+str(e)})

#登录
def login(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        tUser = User(data["userName"])
        
        # 输入的用户名不存在时返回错误
        if tUser.get(["id"])==-1:
            return JsonResponse({"code":1,"userNameExist":False})
        
        # 用户名存在
        encode_password=utils.encoder(data["userPassword"])
        
        # 密码正确
        if tUser.get(["password"]) == encode_password:
            payload={
                "userId":tUser.get(["id"]),
                "my_exp":int(time.time())+EXPIRE_TIME
            }
            Token=utils.generatetoken(payload)
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
        tUser=User(id)
        tUser.deleteUser()
        return JsonResponse({"code":1,"removeOk":True})    
    except Exception as e:
        return JsonResponse({"code":0,"msg":"removeError:"+str(e)})   
    
    
#改变密码
def change_pwd(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))
        new_password = utils.encoder(data["userNewPassword"])
        
        id = request.userid
        tUser=User(id)
        #cursor.execute("select user_password from user where user_id = %s",id)
        if new_password == tUser.get(["password"]):
        # 新密码和原密码相同
            return JsonResponse({"code":1,"duplicatePassword":True})
        else :
            tUser.set({"user_password":new_password})
        #sql_data = [new_password,id]
        #cursor.execute("update user set user_password=%s where user_id=%s",sql_data)
        #connection.commit()
        # 新密码有效
        return JsonResponse({"code":1,"duplicatePassword":False,"updatePassword":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"changePwdError:"+str(e)})


def update(request):
    cursor = connection.cursor()

    try:   
        data = json.loads(request.body.decode("utf-8"))  
        sql_data = [
            data["phone"],
            data["id"]
        ]
        cursor.execute("update user set phone=%s where id=%s",sql_data)
        connection.commit()
        return JsonResponse({"code":1})
    except Exception as e:
        connection.rollback()
        return JsonResponse({"code":0,"msg":"updateError"+str(e)})
    finally:
        cursor.close()




# #ODO:
#     1.生成token的第三方库
#     2.login中生成token
#     3.每次数据访问都检查token