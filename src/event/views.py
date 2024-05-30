
from django.shortcuts import render
import json
#from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
import pymysql

from django.db import connection

from entity.user import User,SuperUser



def create_private_event(request):
    try:
        event_id_now=utils.return_current_event_id(1)

        user = User({"id":request.id})
        data = json.loads(request.body.decode("utf-8"))
        temp_dict = {
            "id":event_id_now,
            "creator_id":user.get(["id"]),
            "name":data["eventName"],
            "start_time":data["eventStartTime"],
            "end_time":data["eventEndTime"],
            "start_date":data["eventStartDate"],
            "end_date":data["eventEndDate"],
            "location":data["eventLocation"],
            "description":data["eventDescription"],
        }
        new_event=user.create_private_event(temp_dict)
        
        # 创建成功
        return JsonResponse({"code":1,"create_Event_Ok":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"createPrivateEventError:"+str(e)})


def load_user_page(request):
    conn=pymysql.connect(host="192.168.43.246",user="sa",password="",db="eventband",port=3306,charset="utf8")
    cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)

    try:
        data = json.loads(request.body.decode("utf-8"))
        cd,potential_id=utils.validtoken(data["userToken"])   
        if cd==1:
            cursor.execute("select er.eurelation_event_id as event_id,er.eurelation_role as role,eb.event_start as event_start,eb.event_end as event_end,eb.event_name as event_name,eb.event_location as event_location,eb.event_description as event_description,eb.event_type as event_type from  (select eurelation_event_id,eurelation_role from eurelation where eurelation_user_id=%s) er  left join event_brief eb on er.eurelation_event_id=eb.event_id",potential_id)
            result=cursor.fetchall()
            return JsonResponse({"code":1,"queryResult":result})
            
        elif cd==2:
            return JsonResponse({"code":1,"msg":potential_id})
        elif cd==0:
            return JsonResponse({"code":0,"msg":potential_id})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"loadUserPageError"+str(e)})
    finally:
        cursor.close()


def get_events(request):
    cursor = connection.cursor()

    try:
        user=SuperUser({"id":request.id})
        event_list = user.get_all_events(cursor)   # 活动对象列表

        return JsonResponse({"code":1,"data":[event.to_dict() for event in event_list]})
    except Exception as e:
        connection.rollback()
        return JsonResponse({"code":0,"msg":"getAllEventsError:"+str(e)})
    finally:
        cursor.close()