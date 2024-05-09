from django.shortcuts import render
import json
from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
import jwt
from event_band.settings import EXPIRE_TIME,SECRET_KEY
import time


def register(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))
        cursor.execute("select user_name from user where user_name=%s",data["userName"])
        if len(cursor.fetchall())>0:
            # 用户名已存在
            return JsonResponse({"code":1,"userNameExist":True})
        sql_data = [
            data["userName"],
            utils.encoder(data["userPassword"])
        ]
        cursor.execute("insert into user (user_name,user_password) values (%s,%s)",sql_data)
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
        data = json.loads(request.body.decode("utf-8"))
        cursor.execute("select user_password,user_id from user where user_name = %s",data["userName"])        
        result = cursor.fetchall()
        if len(result)==0:
            # 用户名不存在
            return JsonResponse({"code":1,"userNameExist":False})      
        password_db = result[0][0]
        encoded_password = utils.encoder(data["userPassword"])
        if password_db == encoded_password:
            # 密码正确
            payload={
                "userId":result[0][1],
                "my_exp":int(time.time())+EXPIRE_TIME
            }
            Token=jwt.encode(payload,SECRET_KEY,algorithm="HS256")
            #cursor.execute("insert into token (token_token) values(%s) ",Token) 
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
        data = json.loads(request.body.decode("utf-8"))
        cd,potential_id=validtoken(data["userToken"])
        if cd==1:
            cursor.execute("delete from user where user_id=%s",potential_id)
            connection.commit()
            return JsonResponse({"code":1,"removeOk":True})
        elif cd==2:
            return JsonResponse({"code":1,"msg":potential_id})
        elif cd==0:
            return JsonResponse({"code":0,"msg":potential_id})
    except Exception as e:
        connection.rollback()
        return JsonResponse({"code":0,"msg":"removeError:"+str(e)})   
    finally:
        cursor.close()
    

def change_pwd(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))
        cd,potential_id=validtoken(data["userToken"])   
        if cd==1:
            cursor.execute("select user_password from user where user_id = %s",potential_id)
            new_password = utils.encoder(data["userNewPassword"])
            old_password=   cursor.fetchall()[0][0]
            if new_password == old_password:
            # 新密码和原密码相同
                return JsonResponse({"code":1,"duplicatePassword":True})
            
       
            sql_data = [new_password,potential_id]
            cursor.execute("update user set user_password=%s where user_id=%s",sql_data)
            connection.commit()
        # 新密码有效
            return JsonResponse({"code":1,"duplicatePassword":False,"updatePassword":True})
        elif cd==2:
            return JsonResponse({"code":1,"msg":potential_id})
        elif cd==0:
            return JsonResponse({"code":0,"msg":potential_id})
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
def validtoken(tok):
    cursor = connection.cursor()
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
    finally:
        cursor.close()



# #ODO:
#     1.生成token的第三方库
#     2.login中生成token
#     3.每次数据访问都检查token