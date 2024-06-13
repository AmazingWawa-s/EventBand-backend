from entity.event import PrivateEvent
from event_band.global_vars import All_conn_dict
from asgiref.sync import async_to_sync
from entity.message import ChatMessage
from entity.user import User
from django.http import JsonResponse
import json

async def send_to_group(data:dict,eid):
    temp_event=PrivateEvent(eid,"select")
    participants:list[dict] = temp_event.get(["participants"])[0]
    creator_id=temp_event.get(["creator_id"])[0]

    global All_conn_dict
    # 发给活动创建者
    if creator_id in All_conn_dict:
        await All_conn_dict[creator_id].send_notification(data)
    # 发给参与者
    for participant in participants:
        print("###### Group sent start! ######")
        if participant["eurelation_user_id"] in All_conn_dict:
            await All_conn_dict[participant["eurelation_user_id"]].send_notification(data)
        print("###### Group sent end! ######")
    

def get_group_messages(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        result=ChatMessage.getGroupMessagesByEid(data["eventId"])

        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getGroupMessagesError:"+str(e)})    
    
def get_private_messages(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        result=ChatMessage.getPrivateMessageByUids(request.userid,data["receiverId"])

        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getPrivateMessagesError:"+str(e)})    
    
def get_all_messages(request):
    try:
        result=ChatMessage.getAllMessages(request.userid)


        return JsonResponse({"code":1, "data":result})
    except Exception as e:
        return JsonResponse({"code":0,"msg":"getAllMessagesError:"+str(e)})      
    
