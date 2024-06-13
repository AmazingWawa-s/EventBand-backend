from entity.event import PrivateEvent
from event_band.utils import All_conn_dict
from asgiref.sync import async_to_sync

async def send_to_group(data:dict,eid):
    temp_event=PrivateEvent(eid,"select")
    participants:list[dict] = temp_event.get(["participants"])[0]

    global All_conn_dict
    for participant in participants:
        print("###### Group sent start! ######")
        if "eurelation_user_id" in All_conn_dict:
            await All_conn_dict[participant["eurelation_user_id"]].send_notification(data)
        print("###### Group sent end! ######")

