
from django.shortcuts import render
import json
#from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
import pymysql
from entity.user import User,SuperUser


def create_private_event(request):
    try:
        user = User(request.userid)
        data = json.loads(request.body.decode("utf-8"))
        temp_dict = {
            "creator_id":user.get(["id"]),
            "name":data["eventName"],
            "start_time":data["eventStartTime"],
            "end_time":data["eventEndTime"],
            "start_date":data["eventStartDate"],
            "end_date":data["eventEndDate"],
            "location_id":data["eventLocationId"],
            "description":data["eventDescription"],
        }
        s=user.create_private_event(temp_dict)
        if s==True:
            return JsonResponse({"code":1,"create_Event_Ok":True})
        elif s==False:
            return JsonResponse({"code":1,"create_Event_Ok":False,"time_collision":True})
        
    except Exception as e:
        return JsonResponse({"code":0,"msg":"createPrivateEventError:"+str(e)})


def load_user_page(request):
    

    try:
        user = User(request.userid)
        data = json.loads(request.body.decode("utf-8"))
        result=user.get_all_locations()
        return JsonResponse({"code":1,"All_Locations":result})
        
    except Exception as e:
        return JsonResponse({"code":0,"msg":"loadUserPageError"+str(e)})
    


def get_created_events(request):

    try:
        user = User(request.userid)
        result=user.get_created_event_id()
        return JsonResponse({"code":1, "data": [i["event_id"] for i in result]})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getCreatedEventsError:"+str(e)})
    

def get_participated_events(request):
    try:
        user = User(request.userid)
        result=user.get_created_event_id()
        return JsonResponse({"code":1, "data": [i["event_id"] for i in result]})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getParticipatedEventsError:"+str(e)})

def delete_event(request):
    try:
        user = User(request.userid)
        data = json.loads(request.body.decode("utf-8"))
        user.delete_event(data["event_id"])
        return JsonResponse({"code":1, "removeOk": True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"deleteEventError:"+str(e)})
    