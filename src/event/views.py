
from django.shortcuts import render
import json
from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils

def add_event(request):
    cursor = connection.cursor()
    try:
        data = json.loads(request.body.decode("utf-8"))
        cd,potential_id=utils.validtoken(data["userToken"])
        
            
    except print(0):
        pass
    return 0

def create_private_event(request):
    cursor = connection.cursor()
    try:
        data = json.loads(request.body.decode("utf-8"))
        cd,potential_id=utils.validtoken(data["userToken"])   
        if cd==1:
            sql_data = [data["eventStart"],data["eventEnd"],data["eventName"],data["eventDescription"]]
            cursor.execute("insert into event (event_start,event_end,event_name,event_description) values (%s,%s,%s,%s)",sql_data)
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