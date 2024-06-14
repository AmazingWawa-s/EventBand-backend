from django.contrib import admin
from django.urls import path
from user import views as uv
from event import views as ev
from django.conf import settings
from django.conf.urls.static import static
from chat import views as cv

urlpatterns = [
    #user
    path("admin/", admin.site.urls),
    path("login/", uv.login),
    path("register/", uv.register),
    path("changepwd/",uv.change_pwd),
    path("logoff/",uv.remove),
    path("getlocations/",uv.get_all_locations),
    path("loaduserpage/",ev.load_user_page),
    path("empty/",uv.empty),

    # su
    path("superlogin/",uv.super_login),
    path("deletelocation/",uv.delete_location),
    path("createlocation/",uv.add_location),
    path("getallevents/",ev.get_all_events),

    # event
    path("createevent/private/",ev.create_private_event),
    path("userpage/",ev.load_user_page),
    path("deleteevent/",ev.delete_event),
    path("eventdetail/",ev.load_event_page),
    path("updatedetail/",ev.update_event_detail),
    path("costremark/add/",ev.add_cost_remark),
    path("costremark/examine/",ev.examine_cost_remark),
    path("joinevent/",ev.join_event),
    path("invite/",ev.invite),
    path("withdraw/",ev.withdraw_event),
    path("deleteparticipant/",ev.delete_participant),
    path("publicevents/",ev.select_public_events),
    path("getexamineevents/",ev.get_examine_events),
    path("examine/",ev.examine_event),
    path("subevent/add/",ev.add_subevent),
    path("subevent/get/",ev.get_subevents),    
    
    # group
    path("group/add/",ev.add_event_group),
    path("group/join/",ev.join_group),

    # resource
    path("resource/add/",ev.add_resource),
    path("resource/delete/",ev.delete_resource),
    path("resource/update/",ev.update_resource),

    # comment
    path("comment/add/",ev.add_comment),
    path("comment/get/",ev.get_comments),


    # chat record
    path("chatrecord/event/",cv.get_group_messages),
    path("chatrecord/private/",cv.get_private_messages),
    path("chatrecord/",cv.get_all_messages),


    path("test/",ev.testtest)
]


# 允许前端直接访问后端media文件夹（不建议，仅DEBUG）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
