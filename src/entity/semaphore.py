# import threading
 
# class Semaphore:
#     def __init__(self, initial_value=1):
#         self.count = initial_value
#         self.lock = threading.Lock()
#         self.condition = threading.Condition(self.lock)
 
#     def acquire(self):
#         with self.condition:
#             while self.count <= 0:
#                 self.condition.wait()
#                 self.count -= 1
 
#     def release(self):
#         with self.condition:
#             self.count += 1
#             self.condition.notify_all()
class Semaphore:
    def __init__(self,initial_value):
        self.count=initial_value
    def P(self):
        while self.count<=0:
            pass
        self.count-=1
    def V(self):
        self.count+=1
        
