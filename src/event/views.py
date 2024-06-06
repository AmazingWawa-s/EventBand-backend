
from django.shortcuts import render
import json
#from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
import pymysql
from entity.user import User,SuperUser
from entity.event import Event,PrivateEvent,PublicEvent

#views.py中的函数名均为小写单词加下划线分隔符
#entity中类的成员函数命名均为第一个单词首字母小写，之后的单词首字母大写，无分割符
#db.py中的函数命名均为第一个单词首字母大写，之后的单词首字母小写，无分割符
#utils.py中的函数命名均为第一个单词首字母大写，之后的单词首字母小写，分隔符为下划线
def create_private_event(request):
    try:
        
        data = json.loads(request.body.decode("utf-8"))
        temp_dict = {
            "creator_id":request.userid,
            "name":data["eventName"],
            "start_time":data["eventStartTime"],
            "end_time":data["eventEndTime"],
            "start_date":data["eventStartDate"],
            "end_date":data["eventEndDate"],
            "location_id":data["eventLocationId"],
            "description":data["eventDescription"],
        }
        s=User.create_private_event(request.userid,temp_dict)
        if s==True:
            return JsonResponse({"code":1,"create_Event_Ok":True})
        elif s==False:
            return JsonResponse({"code":1,"create_Event_Ok":False,"time_collision":True})
        
    except Exception as e:
        return JsonResponse({"code":0,"msg":"createPrivateEventError:"+str(e)})


def load_user_page(request):
    try:
        res={}
        
        tempuser=User(request.userid,"select")
        result_events=tempuser.getEvents()
        
        result_locations=tempuser.getLocations()

        
        res["eventlist"]=result_events
        res["locationlist"]=result_locations
        return JsonResponse({"code":1, "data": res})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"loadUserPageError:"+str(e)})
    

def get_all_events(request):
    try:
        su=SuperUser(request.userid,"classattrs")
        result=su.getAllEvents()
        return JsonResponse({"code":1,"data":result}) 
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getAllEventsError:"+str(e)})



def delete_event(request):
    try:
        user = User(request.userid,"delete")
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
        result={}
        
        # 参与者列表：包括用户id和名称
        participant_list=[]
        for participant_id in temp_event.get(["participants"])[0]:
            temp_dict={}
            temp_dict["id"]=participant_id
            temp_dict["name"]=User(participant_id).get(["name"])[0]
            participant_list.append(temp_dict)
        result["participants"]=participant_list



        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getPrivateEventDetailError:"+str(e)})
    
def delete_participant(request):
    data = json.loads(request.body.decode("utf-8"))
    

        