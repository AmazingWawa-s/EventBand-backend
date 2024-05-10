from django.shortcuts import render
import json
from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
from event_band.settings import EXPIRE_TIME
import time
from classes.user import User


def register(request):

    cursor = connection.cursor()

    try:
        
        tempUser = User(request)
        
        cursor.execute("select user_name from user where user_name=%s",tempUser.get(["name"]))
        if len(cursor.fetchall())>0:
            # 用户名已存在
            return JsonResponse({"code":1,"userNameExist":True})

        cursor.execute("insert into user (user_name,user_password) values (%s,%s)",tempUser.get(["name","password"]))
        connection.commit()
        # 注册成功
        return JsonResponse({"code":1,"userNameExist":False,"register_ok":True})
    except Exception as e:
        connection.rollback()
        return JsonResponse({"code":0,"msg":"registerError:"+str(e)})
    finally:
        cursor.close()


def login(request):
    cursor = connection.cursor()

    try:
        
        
        tempUser = User(request)
        
        cursor.execute("select user_password,user_id from user where user_name = %s",tempUser.get(["name"]))
            
        result = cursor.fetchall()
        
        if len(result)==0:
            # 用户名不存在
            return JsonResponse({"code":1,"userNameExist":False})   
        
        dbUser = User()
        dbUser.set(["id","password"],[result[0][1],result[0][0]])
        
        if tempUser.get(["password"]) == dbUser.get(["password"]):
            # 密码正确
            payload={
                "userId":dbUser.get(["id"]),
                "my_exp":int(time.time())+EXPIRE_TIME
            }
            Token=utils.generatetoken(payload)
            return JsonResponse({"code":1,"userNameExist":True,"userPasswordOk":True,"userToken":Token})
        else:
            # 密码错误
            return JsonResponse({"code":1,"userNameExist":True,"userPasswordOk":False})     
    except Exception as e:
        return JsonResponse({"code":0,"msg":"loginError:"+str(e)})
    finally:
        cursor.close()
 

def remove(request):
    cursor = connection.cursor()
    try:
        id = request.userid
        cursor.execute("delete from user where user_id=%s",id)
        connection.commit()
        return JsonResponse({"code":1,"removeOk":True})

        
    except Exception as e:
        connection.rollback()
        return JsonResponse({"code":0,"msg":"removeError:"+str(e)})   
    finally:
        cursor.close()
    

def change_pwd(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))
        id = request.userid
        cursor.execute("select user_password from user where user_id = %s",id)
        new_password = utils.encoder(data["userNewPassword"])
        old_password=   cursor.fetchall()[0][0]
        if new_password == old_password:
        # 新密码和原密码相同
            return JsonResponse({"code":1,"duplicatePassword":True})
            
       
        sql_data = [new_password,id]
        cursor.execute("update user set user_password=%s where user_id=%s",sql_data)
        connection.commit()
        # 新密码有效
        return JsonResponse({"code":1,"duplicatePassword":False,"updatePassword":True})
    except Exception as e:
        connection.rollback()
        return JsonResponse({"code":0,"msg":"changePwdError:"+str(e)})
    finally:
        cursor.close()


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