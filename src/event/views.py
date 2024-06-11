
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
        s,eid=User.createPrivateEvent(request.userid,temp_dict)
        if s==1:
            return JsonResponse({"code":1,"create_Event_Ok":True,"create_Event_Id":eid})
        elif s==0:
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
        user.deleteEvent(data["eventId"])
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

def load_event_page(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        temp_event=PrivateEvent(data["eventId"],"select")
        participants=temp_event.get(["participants"])[0]
        eventdetail=temp_event.get(["detail"])[0]
        # 参与者列表：包括用户id和名称
    
        result={
            "participants":participants,
            "eventdetail":eventdetail
        }



        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"loadEventPageError:"+str(e)})
    
def update_event_detail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        temp_event=PrivateEvent(data["eventId"],"update")
        temp_event.set(data["eventDetail"])
        


        return JsonResponse({"code":1, "updateDetailOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"updateEventDetailError:"+str(e)})

def invite(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        code=utils.Generate_invite_id(data["eventId"])
        


        return JsonResponse({"code":1, "inviteCode":code})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"inviteError:"+str(e)})

def join_event(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        event_id=utils.Get_id(data["inviteCode"])
        if event_id == -1:
            return JsonResponse({"code":1, "msg":"Invalid Invite Code"})
        
        temp_event=PrivateEvent(event_id,"join")

        result=temp_event.joinEvent(event_id,request.userid)

        if result == 0:
            return JsonResponse({"code":1, "msg":"Already joined","eventId":event_id})
        elif result==2:
            return JsonResponse({"code":1, "msg":"event already full"})
        temp_event.__del__()
        


        return JsonResponse({"code":1, "ValidInviteCode":True,"joinOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"joinError:"+str(e)})
   
def withdraw_event(request):
    try:
        uid=request.userid
        data = json.loads(request.body.decode("utf-8"))
        temp_event=PrivateEvent(data["eventId"],"select")

        if temp_event.get(["creator_id"])[0]==uid:
            return JsonResponse({"code":1, "msg":"creator can't withdraw, use delete","withdrawOk":False})
        elif uid not in temp_event.get(["par_id"])[0]:
            return JsonResponse({"code":1, "msg":"not in event","withdrawOk":False})
        
        Event.deleteParticipant(uid,data["eventId"])

        return JsonResponse({"code":1, "withdrawOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"withdrawError:"+str(e)})  

def delete_participant(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        temp_event=PrivateEvent(data["eventId"],"select")
        if temp_event.get(["creator_id"])[0] != request.userid:
            return JsonResponse({"code":1, "msg":"only creator can delete participant","deleteOk":False})
        
        Event.deleteParticipant(data["userId"],data["eventId"])

        return JsonResponse({"code":1, "deleteOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"deleteParticipantError:"+str(e)})            
    
def select_public_events(request):
    try:
        result=User.getPublicEvents()
        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"selectPublicEventError:"+str(e)}) 