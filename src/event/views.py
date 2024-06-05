
from django.shortcuts import render
import json
#from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
import pymysql
from entity.user import User,SuperUser
from entity.event import Event,PrivateEvent,PublicEvent


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
        result_created=user.get_created_event()
        # if len(result1)==0:
        #     return JsonResponse({"code":1, "have_no_created_event": True})
        result_participated=user.get_participated_event()
        # if len(result2)==0:
        #     return JsonResponse({"code":1, "have_no_participated_event": True})
        result_locations=user.get_all_locations()

        result={}
        result["created"]=result_created
        result["participated"]=result_participated
        result["locationList"]=result_locations
        return JsonResponse({"code":1, "data": result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"loadUserPageError:"+str(e)})
    

def get_all_events(request):
    try:
        su=SuperUser(request.userid)
        result=su.get_all_events()
        return JsonResponse({"code":1,"data":[i.to_dict() for i in result]}) 
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getAllEventsError"+str(e)})

def get_created_events(request):

    try:
        user = User(request.userid)
        result=user.get_created_event()
        if len(result)==0:
            return JsonResponse({"code":1, "have_no_created_event": True})
        
        return JsonResponse({"code":1, "data": result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getCreatedEventsError:"+str(e)})
    

def get_participated_events(request):
    try:
        user = User(request.userid)
        result=user.get_participated_event()
        if len(result)==0:
            return JsonResponse({"code":1, "have_no_participated_event": True})
        
        return JsonResponse({"code":1, "data": result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getParticipatedEventsError:"+str(e)})

def delete_event(request):
    try:
        user = User(request.userid)
        data = json.loads(request.body.decode("utf-8"))
        user.delete_event(data["eventId"])
        return JsonResponse({"code":1, "removeOk": True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"deleteEventError:"+str(e)})

def get_invite_code(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        result=utils.get_invite_code(data["eventId"])
        return JsonResponse({"code":1, "inviteCode":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getInviteCodeError:"+str(e)})

def private_event_detail_page(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        temp_event=PrivateEvent(data["eventId"],"select")
        result=temp_event.to_dict()
        
        # 参与者列表：包括用户id和名称
        participant_list=[]
        for participant_id in temp_event.get(["participants"])[0]:
            temp_dict={}
            temp_dict["id"]=participant_id
            temp_dict["name"]=User(participant_id).get(["name"])[0]
            participant_list.append(temp_dict)
        result["participants"]=participant_list

        # 用户在活动中的身份
        result["role"]=temp_event.get_user_role(request.userid)

        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getPrivateEventDetailError:"+str(e)})
        