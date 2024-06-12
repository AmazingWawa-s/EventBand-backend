from django.apps import AppConfig
from event_band.utils import Count_event,Count_location,Count_group


class EventConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "event"
    def ready(self):
        Count_event() 
        Count_location()
        Count_group()
# your_app/apps.py
 

 
class YourAppConfig(AppConfig):
    name = 'yourapp'
 
    def ready(self):
        Count_event()
        Count_location()
        Count_group()
        
        # 在这里调用你想要在启动时运行的函数
        
 
 