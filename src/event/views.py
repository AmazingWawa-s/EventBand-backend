
from django.shortcuts import render
import json
from django.db import connection
from django.http import JsonResponse
import event_band.utils as utils

def add_event(request):
    cursor = connection.cursor()
    try:
        data = json.loads(request.body.decode("utf-8"))
        cd,potential_id=utils.validtoken(data["userToken"])
        
            
    except print(0):
        pass
    return 0