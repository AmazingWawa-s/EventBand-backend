from django.apps import AppConfig
from event_band.utils import Count_event,Count_location


class EventConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "event"
    def ready(self):
        Count_event() 
        Count_location()
# your_app/apps.py
 

 
class YourAppConfig(AppConfig):
    name = 'yourapp'
 
    def ready(self):
        Count_event()
        Count_location()
        
        # 在这里调用你想要在启动时运行的函数
        
 
 