
from django.shortcuts import render
import json
#from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils
import pymysql
from entity.user import User,SuperUser
from entity.event import Event,PrivateEvent,PublicEvent
from entity.group import Group
from entity.costremark import Costremark
from entity.message import Message
from entity.resource import Resource
from entity.comment import Comment
from entity.subevent import Subevent
from event_band.global_vars import All_conn_dict
from asgiref.sync import async_to_sync
from datetime import datetime

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
            "location":data["eventLocation"],
            "description":data["eventDescription"],
            "type":data["eventType"],
            "person_num":data["personNum"]
        }
        user=User(request.userid,"classattrs")
        s=user.createPrivateEvent(temp_dict)
        if s==1:
            return JsonResponse({"code":1,"create_Event_Ok":True,"msg":"正常创建"})
        elif s==0:
            return JsonResponse({"code":1,"create_Event_Ok":False,"time_collision":True})
        elif s==2:
            return JsonResponse({"code":1,"create_Event_Ok":True,"msg":"抢占成功"})
        
    except Exception as e:
        return JsonResponse({"code":0,"msg":"createPrivateEventError:"+str(e)})


def load_user_page(request):
    try:
        res={}
        tempuser=User(request.userid,"select")
        result_events=tempuser.getEvents()
        result_locations=tempuser.getLocations()
        todolist=Message.getUserMessage(request.userid)
        res["eventlist"]=result_events
        res["locationlist"]=result_locations
        res["todolist"]=todolist
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



def load_event_page(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        temp_event=PrivateEvent(data["eventId"],"select")

        eventbrief=temp_event.get(["event_brief"])[0]

        
        temp_event.getFromEUDB()
        participants=temp_event.get(["participants"])[0]
        
        temp_event.getFromEventDetail()
        eventdetail=temp_event.get(["detail"])[0]
        
        temp_event.getEventGroups()
        eventgroups=temp_event.get(["groups"])[0]
        
        temp_event.getEventResource()
        eventresources=temp_event.get(["resources"])[0]
        
        costremarks=Costremark.getAllRemarks(data["eventId"])

        subevents=Subevent.getSubevent(data["eventId"])

        # 参与者列表：包括用户id和名称
    
        result={
            "eventbrief":eventbrief,
            "subevents":subevents,
            "participants":participants,
            "eventdetail":eventdetail,
            "costRemarks":costremarks,
            "groups":eventgroups,
            "resources":eventresources
        }



        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"loadEventPageError:"+str(e)})
    
def update_event_detail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        if request.userid==utils.checkEventCreator(data["eventId"]):
            temp_event=PrivateEvent(data["eventId"],"update")
            temp_event.set(data["eventDetail"])
            temp_event.set(data["eventBrief"])
            return JsonResponse({"code":1, "updateDetailOk":True})
        else:
            return JsonResponse({"code":1, "updateDetailOk":False,"msg":"only creator can update event"})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"updateEventDetailError:"+str(e)})

def invite(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        if request.userid==utils.checkEventCreator(data["eventId"]):
            code=utils.Generate_invite_id(data["eventId"])
            return JsonResponse({"code":1, "inviteCode":code})
        else:
            return JsonResponse({"code":1, "inviteCode":-1,"msg":"only creator can invite"})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"inviteError:"+str(e)})

def join_event(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        
        event_id=utils.Get_id(data["inviteCode"])
        if event_id == -1:
            return JsonResponse({"code":1, "msg":"Invalid Invite Code"})
        
        temp_event=PrivateEvent(event_id,"join")
        
        if temp_event.get(["creator_id"])!=request.userid:

            result=temp_event.joinEvent(event_id,request.userid)

            if result == 0:
                return JsonResponse({"code":1, "msg":"Already joined","eventId":event_id})
            elif result==2:
                return JsonResponse({"code":1, "msg":"event already full"})
            temp_event.__del__()
            
            return JsonResponse({"code":1, "ValidInviteCode":True,"joinOk":True})
        else:
            return JsonResponse({"code":1, "ValidInviteCode":True,"joinOk":False})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"joinEventError:"+str(e)})
   
def withdraw_event(request):
    try:
        uid=request.userid
        data = json.loads(request.body.decode("utf-8"))
        temp_event=PrivateEvent(data["eventId"],"select")

        if temp_event.get(["creator_id"])[0]==uid:
            return JsonResponse({"code":1, "msg":"creator can't withdraw, use delete","withdrawOk":False})
        elif uid not in temp_event.get(["par_id"])[0]:
            return JsonResponse({"code":1, "msg":"not in the event","withdrawOk":False})
        
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
    
def get_examine_events(request):
    try:
        su=SuperUser(request.userid,"classattrs")
        result=su.getExamineEvents()
        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getExamineEventsError:"+str(e)})    
    
def examine_event(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        su=SuperUser(request.userid,"classattrs")
        if data["passed"]==True:
            su.examineEvent(data["examineEventId"])
            return JsonResponse({"code":1, "examineOk":True})
        else:
            su.denyEvent(data["examineEventId"],data["reason"])
            return JsonResponse({"code":1, "examineOk":False})

    except Exception as e:
        return JsonResponse({"code":0,"msg":"examineEventError:"+str(e)})        
def add_event_group(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        if utils.checkEventCreator(data["groupEventId"])==request.userid:
            tg=Group(-1,"create")
            gid=utils.Return_current_group_id(1)
            tg.set({"group_id":gid,"group_name":data["groupName"],"group_event_id":data["groupEventId"]})
            return JsonResponse({"code":1, "createGroupOk":True,"groupId":gid})
        else:
            return JsonResponse({"code":1, "createGroupOk":False,"groupId":-1})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"addEventGroupError:"+str(e)}) 
def join_group(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        if utils.checkEventCreator(data["groupEventId"])==request.userid:
            Group.joinGroup(data["groupId"],data["groupEventId"],data["groupUserId"])
            return JsonResponse({"code":1, "joinGroupOk":True})
        else:
            return JsonResponse({"code":1, "joinGroupOk":False,"msg":"creator can't join group"})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"joinGroupError:"+str(e)}) 
    
def add_cost_remark(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        temp_event=PrivateEvent(data["eventId"],"select")
        temp_event.getFromEUDB()
        if request.userid not in temp_event.get(["par_id"])[0]:
            return JsonResponse({"code":1, "addCostRemarkOk":False,"msg":"Only participants can add cost remark"})
        
        remark=Costremark(-1,"create")
        temp_dict={
            "cr_event_id":data["eventId"],
            "cr_user_id":request.userid,
            "cr_cost":data["cost"],
            "cr_reason":data["reason"]
        }
        remark.set(temp_dict)
        creator_id=utils.checkEventCreator(data["eventId"])
        Message(creator_id,"新的预算报销申请！","link","/eventDetail?id="+data["eventId"],"")
        return JsonResponse({"code":1, "addCostRemarkOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"addCostRemarkError:"+str(e)}) 

    
def examine_cost_remark(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        remark=Costremark(data["costRemarkId"],"update")
        remark.set({"cr_passed":data["passed"],"cr_remark":data["remark"]})
        user_id=Costremark.selectUidById(data["costRemarkId"])
        event_id=Costremark.selectEidById(data["costRemarkId"])
        if data["passed"]=="true":
            Message(user_id[0]["cr_user_id"],"预算报销成功！","link","/eventDetail?id="+str(event_id[0]["cr_event_id"]),data["remark"])
        else:
            Message(user_id[0]["cr_user_id"],"预算报销被驳回！","link","/eventDetail?id="+str(event_id[0]["cr_event_id"]),data["remark"])
        #temp_event=PrivateEvent(data["eventId"],"join")
        return JsonResponse({"code":1, "examineOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"examineCostRemarkError:"+str(e)})     
    

def testtest(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        temp_dict={
            "message":"you get my message!!!!!",
        }
        global All_conn_dict
        if request.userid in All_conn_dict:
            async_to_sync(All_conn_dict[request.userid].send_notification)(temp_dict)
            #utils.notify_user(request.userid,temp_dict)

        return JsonResponse({"code":1, "testtestOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"testtestError:"+str(e)})       
    
def add_resource(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        if utils.checkEventCreator(data["resourceEventId"])==request.userid:#只有活动的创建者才能为活动添加资源
            tr=Resource(-1,"create")
            rid=utils.Return_current_group_id(1)
            tr.set({"resource_id":rid,"resource_name":data["resourceName"],"resource_eid":data["resourceEventId"],"resource_condition":data["resourceCondition"],"resource_num":data["resourceNum"]})
            return JsonResponse({"code":1, "createResourceOk":True,"resourceId":rid})
        else:
            return JsonResponse({"code":1, "createResourceOk":False,"msg":"only event's creator can add resource"})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"addResourceError:"+str(e)}) 
def delete_resource(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        
        if utils.checkEventCreator(data["eventId"])==request.userid:#只有活动的创建者才能为活动添加资源
            tr=Resource(data["resourceId"],"delete")
            return JsonResponse({"code":1, "deleteResourceOk":True})
        else:
            return JsonResponse({"code":1, "createResourceOk":False,"msg":"only event's creator can delete resource"})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"deleteResourceError:"+str(e)}) 

def update_resource(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        if utils.checkEventCreator(data["eventId"])==request.userid:#只有活动的创建者才能更新资源
            tr=Resource(data["resourceId"],"update")
            tr.set(data["toUpdate"])
            return JsonResponse({"code":1, "updateResourceOk":True})
        else:
            return JsonResponse({"code":1, "updateResourceOk":False,"msg":"only event's creator can update resource"})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"updateResourceError:"+str(e)}) 
    
def add_comment(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        time=datetime.fromtimestamp(float(data["time"]))
        Comment(request.userid,data["content"],data["eventId"],time)

        return JsonResponse({"code":1, "addCommentOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"addCommentError:"+str(e)}) 
    
def get_comments(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        result=Comment.getComments(data["eventId"])

        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getCommentsError:"+str(e)})    
    

def add_subevent(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        Subevent(data["eventId"],data["time"],data["title"],data["content"],data["participants"])

        return JsonResponse({"code":1, "addOk":True})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"addSubeventError:"+str(e)})

def get_subevents(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        result=Subevent.getSubevent(data["eventId"])

        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getSubeventError:"+str(e)})    
    