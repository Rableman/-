#coding utf-8
import map_proc

class common_data:
    def __init__(self,device_num):
        self.Device_sum = device_num
        self.Goal_field = list()
    
    def ret_dev_sum(self):
        return self.Device_sum
    
    def ret_goal_field(self):
        return self.Goal_field
