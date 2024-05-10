
from django.shortcuts import render
import json
from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
import pymysql



def create_private_event(request):
    cursor = connection.cursor()
    try:
        data = json.loads(request.body.decode("utf-8"))
        cd,potential_id=utils.validtoken(data["userToken"])   
        if cd==1:
            event_id_now=utils.return_event_id()
            utils.add_event_id(1)
            #更新活动简略表
            sql_data = [event_id_now,data["eventStart"],data["eventEnd"],data["eventName"],data["eventLocation"],data["eventDescription"]]
            cursor.execute("insert into event_brief (event_id,event_start,event_end,event_name,event_location,event_description,event_type) values (%s,%s,%s,%s,%s,%s,1)",sql_data)
            #更新活动详情表
            sql_data = [event_id_now]
            cursor.execute("insert into event_detail (event_id) values (%s)",sql_data)
            #更新活动用户关系表
            sql_data=[event_id_now,potential_id]
            cursor.execute("insert into eurelation (eurelation_event_id,eurelation_user_id,eurelation_role) values(%s,%s,1)",sql_data)
            connection.commit()
            # 创建成功
            return JsonResponse({"code":1,"create_Event_Ok":True})
            
        elif cd==2:
            return JsonResponse({"code":1,"msg":potential_id})
        elif cd==0:
            return JsonResponse({"code":0,"msg":potential_id})
    except Exception as e:
        connection.rollback()
        return JsonResponse({"code":0,"msg":""+str(e)})
    finally:
        cursor.close()
def load_user_page(request):
    conn=pymysql.connect(host="192.168.43.246",user="sa",password="",db="eventband",port=3306,charset="utf8")
    cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)

    try:
        data = json.loads(request.body.decode("utf-8"))
        cd,potential_id=utils.validtoken(data["userToken"])   
        if cd==1:
            cursor.execute("select er.eurelation_event_id as event_id,er.eurelation_role as role,eb.event_start as event_start,eb.event_end as event_end,eb.event_name as event_name,eb.event_location as event_location,eb.event_description as event_description,eb.event_type as event_type from  (select eurelation_event_id,eurelation_role from eurelation where eurelation_user_id=%s) er  left join event_brief eb on er.eurelation_event_id=eb.event_id",potential_id)
            result=cursor.fetchall()
            # result_dict={}
            # for i in result:

            #     result_dict.append()
            return JsonResponse({"code":1,"queryResult":result})
            
        elif cd==2:
            return JsonResponse({"code":1,"msg":potential_id})
        elif cd==0:
            return JsonResponse({"code":0,"msg":potential_id})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"loadUserPageError"+str(e)})
    finally:
        cursor.close()