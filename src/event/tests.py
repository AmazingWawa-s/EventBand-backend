from django.test import TestCase
import random
import string
import jwt

import sys
sys.path.append('/Users/sunxuanye/Desktop/SE/Procedure9/EventBand-backend/src/')
import event_band.utils as utils



# Create your tests here.
def generate_invite_id(id,length=10):
    prefix = hex(int(id))[2:]+ 'L'
    length = length - len(prefix)
    chars=string.ascii_letters+string.digits
    return prefix + ''.join([random.choice(chars) for i in range(length)])

def get_id(code):
    ''' Hex to Dec '''
    print(code.upper())
    return str(int(code.upper(), 16))



s_set = string.ascii_letters + string.digits
raw_code_len = 8
 

class Test():
    def __init__(self):
        self.a=1
        self.b=3
        self.c=2



    # a=generate_invite_id(100,10)
    # print(a.upper())
    # print(a)
    # print(int(a.upper(),16))

te=Test()
if utils.exist(te,["a","s"]):
    print("yes")
else:print("no")
    
    
    
    