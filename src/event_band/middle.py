from django.urls import reverse

import jwt
import json

from django.http import JsonResponse, HttpResponseRedirect
 

from event_band.settings import SECRET_KEY
import time
try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object
 
# 白名单，表示请求里面的路由时不验证登录信息
API_WHITELIST = ['/login/',"/register/"]
class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            if not any(api in request.path for api in API_WHITELIST):
                # if request.path not in API_WHITELIST:
                # 从请求头中获取 username 和 token
                data = json.loads(request.body.decode("utf-8"))
                token = data["userToken"]
                decode_token=jwt.decode(token,SECRET_KEY,algorithms="HS256")
                exp_time=int(decode_token["my_exp"])
                if time.time() >exp_time:
                    return JsonResponse({'code': 1, 'msg': 'token out of date1'})
                else :
                    
                    request.userid=decode_token["userId"]
                    return None
        except Exception as e:
            return JsonResponse({'code': 0, "msg":'ValidTokenError:'+str(e)})
            


