from django.contrib import admin
from django.urls import path
from user import views as uv
from event import views as ev
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #user
    path("admin/", admin.site.urls),
    path("login/", uv.login),
    path("register/", uv.register),
    path("changepwd/",uv.change_pwd),
    path("logoff/",uv.remove),
    path("getlocations/",uv.get_all_locations),
    path("loaduserpage/",ev.load_user_page),

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
    path("joinevent/",ev.join_event),
    path("invite/",ev.invite),
    path("withdraw/",ev.withdraw_event),
    path("deleteparticipant/",ev.delete_participant)
]


# 允许前端直接访问后端media文件夹（不建议，仅DEBUG）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
