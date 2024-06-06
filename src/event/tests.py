#from django.test import TestCase
import random
import string
#import jwt

import sys
sys.path.append('/Users/sunxuanye/Desktop/SE/Procedure9/EventBand-backend/src/')
import event_band.utils as utils



# Create your tests here.
def generate_invite_id(id,length=10):
    prefix = hex(id+100)[2:]+ 'L'
    length = length - len(prefix)
    chars=string.ascii_letters+string.digits
    result=prefix + ''.join([random.choice(chars) for i in range(length)])
    result=result[::-1]
    return result

def get_id(code):
    ori=code[::-1]
    temp=""
    for i in code:
        if i.isupper():
            temp=i
    a=ori.split(temp)[0]
    return str(int(a, 16))

s_set = string.ascii_letters + string.digits
raw_code_len = 8

tid=100
res=generate_invite_id(100,10)



 


    
    
    
    