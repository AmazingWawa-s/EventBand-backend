from django.contrib import admin
from django.urls import path
from user import views as uv
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", uv.login),
    path("register/", uv.register),
    path("changepwd/",uv.change_pwd),
    path("user/update/",uv.update),
    path("user/remove/",uv.remove)
]


# 允许前端直接访问后端media文件夹（不建议，仅DEBUG）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
