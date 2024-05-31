from django.contrib import admin
from django.urls import path
from user import views as uv
from event import views as ev
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", uv.login),
    path("superlogin/",uv.super_login),
    path("register/", uv.register),
    path("changepwd/",uv.change_pwd),
    path("logoff/",uv.remove),
    path("getlocations/",uv.get_all_locations),
    path("deletelocation/",uv.delete_location),
    path("createlocation/",uv.add_location),

    path("createevent/private/",ev.create_private_event),
    path("userpage/",ev.load_user_page),
    path("getevents/created/",ev.get_created_events),
    path("getevents/participated/",ev.get_participated_events),
    path("deleteevent/",ev.delete_event)
]


# 允许前端直接访问后端media文件夹（不建议，仅DEBUG）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
