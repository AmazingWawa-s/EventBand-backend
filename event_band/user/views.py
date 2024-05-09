from django.shortcuts import render
import json
from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
import jwt

def register(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))
        cursor.execute("select user_name from user where user_name=%s",data['userName'])
        print(1)
        if len(cursor.fetchall())>0:
            # 用户名已存在
            return JsonResponse({'code':1,'userNameExist':True})
        print(2)
        sql_data = [
            data['userName'],
            utils.encoder(data['userPassword'])
        ]
        cursor.execute("insert into user (user_name,user_password) values (%s,%s)",sql_data)
        print(3)
        connection.commit()
        print(4)
        # 注册成功
        return JsonResponse({'code':1,'userNameExist':False})
    except Exception as e:
        connection.rollback()
        return JsonResponse({'code':0,'msg':"registerError:"+str(e)})
    finally:
        cursor.close()


def login(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))
        cursor.execute("select user_password,user_id from user where user_name = %s",data['userName'])        
        result = cursor.fetchall()
        if len(result)==0:
            # 用户名不存在
            return JsonResponse({'code':1,'userNameExist':False})      
        
        password_db = result[0][0]
        encoded_password = utils.encoder(data['userPassword'])
        if password_db == encoded_password:
            # 密码正确
            payload={
                "userName":data['userName']
            }
            Token=jwt.encode(payload,'secret',algorithm="HS256")
            cursor.execute("insert into token (token_token) values(%s) ",Token) 
            return JsonResponse({'code':1,'userNameExist':True,'userPasswordOk':True,'userToken':Token})
        else:
            # 密码错误
            return JsonResponse({'code':1,'userNameExist':True,'userPasswordOk':False})     
    except Exception as e:
        return JsonResponse({'code':0,'msg':"loginError:"+str(e)})
    finally:
        cursor.close()
 

def remove(request):
    cursor = connection.cursor()


    try:
        data = json.loads(request.body.decode("utf-8"))
        if validtoken(data['userToken'],data['userId'])==1:
            cursor.execute("delete from user where user_id=%s",data['userId'])
            connection.commit()
            return JsonResponse({'code':1,'removeOk':True})
        elif validtoken(data['userToken'],data['userId'])==2:
            return JsonResponse({'code':2,'msg':'validError'})
        elif validtoken(data['userToken'],data['userId'])==0:
            return JsonResponse({'code':2,'validToken':False})
    except Exception as e:
        connection.rollback()
        return JsonResponse({'code':0,'msg':"removeError:"+str(e)})   
    finally:
        cursor.close()
    

def change_pwd(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))   
        if validtoken(data['userToken'],data['userId'])==1:
            cursor.execute("select user_password from user where user_id = %s",data['userId'])
            new_password = utils.encoder(data['password'])
            old_password=   cursor.fetchall()[0][0]
            if new_password == old_password:
            # 新密码和原密码相同
                return JsonResponse({'code':1,'duplicatePassword':True})

       
            sql_data = [utils.encoder(data["userPassword"]),data['userId']]
            cursor.execute("update user set user_password=%s where user_id=%s",sql_data)
            connection.commit()
        # 新密码有效
            return JsonResponse({'code':1,"duplicatePassword":False,"updatePassword":True})
        elif validtoken(data['userToken'],data['userId'])==2:
            return JsonResponse({'code':2,'msg':'validError'})
        elif validtoken(data['userToken'],data['userId'])==0:
            return JsonResponse({'code':2,'validToken':False})
    except Exception as e:
        connection.rollback()
        return JsonResponse({'code':0,'msg':"changePwdError:"+str(e)})
    finally:
        cursor.close()


def update(request):
    cursor = connection.cursor()

    try:   
        data = json.loads(request.body.decode("utf-8"))  
        sql_data = [
            data['phone'],
            data['id']
        ]
        cursor.execute("update user set phone=%s where id=%s",sql_data)
        connection.commit()
        return JsonResponse({'code':1})
    except Exception as e:
        connection.rollback()
        return JsonResponse({'code':0,'msg':"updateError"+str(e)})
    finally:
        cursor.close()
def validtoken(tok):
    cursor = connection.cursor()
    try:   
        
        
        cursor.execute("select count(*) from token where token_token=%s",tok)
        result = cursor.fetchall()
        if result[0][0]==1:
            return 1
        else :return 0
    except Exception as e:
        connection.rollback()
        return 2
    finally:
        cursor.close()



# #ODO:
#     1.生成token的第三方库
#     2.login中生成token
#     3.每次数据访问都检查token