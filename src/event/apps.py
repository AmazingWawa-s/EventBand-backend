from django.apps import AppConfig
from event_band.utils import count_event,count_location


class EventConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "event"
    def ready(self):
        count_event()
        count_location()
# your_app/apps.py
 

 
class YourAppConfig(AppConfig):
    name = 'yourapp'
 
    def ready(self):
        count_event()
        count_location()
        
        # 在这里调用你想要在启动时运行的函数
        
 
 