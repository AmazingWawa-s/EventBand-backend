from django.shortcuts import render
import json
from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils

def register(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))
        cursor.execute("select id from user where username=%s",data['username'])
        if len(cursor.fetchall())>0:
            # 用户名已存在
            return JsonResponse({'code':1,'username_ok':False})
        
        sql = "insert into user (username,password,phone) values (%s,%s,%s)"
        sql_data = [
            data['username'],
            utils.Encoder(data['password']),
            data['phone']
        ]
        cursor.execute(sql,sql_data)
        connection.commit()
        # 注册成功
        return JsonResponse({'code':1,'username_ok':True})
    except Exception as e:
        connection.rollback()
        return JsonResponse({'code':0,'msg':"注册异常，详细信息："+str(e)})
    finally:
        cursor.close()


def login(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))
        cursor.execute("select password,id from user where username = %s",data['username'])        
        result = cursor.fetchall()
        if len(result)==0:
            # 用户名不存在
            return JsonResponse({'code':1,'username_ok':False})      
        
        password_db = result[0][0]
        encoded_password = utils.Encoder(data['password'])
        if password_db == encoded_password:
            # 密码正确
            return JsonResponse({'code':1,'username_ok':True,'password_ok':True,'id':result[0][1]})
        else:
            # 密码错误
            return JsonResponse({'code':1,'username_ok':True,'password_ok':False})     
    except Exception as e:
        return JsonResponse({'code':0,'msg':"登录异常，详细信息："+str(e)})
    finally:
        cursor.close()
 

def remove(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))
        cursor.execute("delete from user where id=%s",data['id'])
        connection.commit()
        return JsonResponse({'code':1,'msg':"删除用户成功！"})
    except Exception as e:
        connection.rollback()
        return JsonResponse({'code':0,'msg':"删除异常，详细信息："+str(e)})   
    finally:
        cursor.close()
    

def change_pwd(request):
    cursor = connection.cursor()

    try:
        data = json.loads(request.body.decode("utf-8"))   
        cursor.execute("select password from user where id = %s",data['id'])
        new_password = utils.Encoder(data['password'])   
        if new_password == (cursor.fetchall())[0][0]:
            # 新密码和原密码相同
            return JsonResponse({'code':1,'same_password':True})

        sql = "update user set password=%s where id=%s"
        sql_data = [
            utils.Encoder(data["password"]),
            data['id']
        ]
        cursor.execute(sql,sql_data)
        connection.commit()
        # 新密码有效
        return JsonResponse({'code':1,'same_password':False})
    except Exception as e:
        connection.rollback()
        return JsonResponse({'code':0,'msg':"修改密码异常，详细信息："+str(e)})
    finally:
        cursor.close()


def update(request):
    cursor = connection.cursor()

    try:   
        data = json.loads(request.body.decode("utf-8"))  
        sql = "update user set phone=%s where id=%s"
        sql_data = [
            data['phone'],
            data['id']
        ]
        cursor.execute(sql,sql_data)
        connection.commit()
        return JsonResponse({'code':1})
    except Exception as e:
        connection.rollback()
        return JsonResponse({'code':0,'msg':"修改用户信息信息异常，详细信息："+str(e)})
    finally:
        cursor.close()


# #ODO:
#     1.生成token的第三方库
#     2.login中生成token
#     3.每次数据访问都检查token