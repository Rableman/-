#coding utf-8
import map_proc

class common_data:
    def __init__(self,device_num,h,w):
        self.Device_sum = device_num #デバイスの総数
        self.Goal_field = list() #ゴールのフィールド
        self.H = h #H*Wのフィールド
        self.W = w
    
    def ret_dev_sum(self):
        return self.Device_sum
    
    def ret_goal_field(self):
        return self.Goal_field
        
    def set_start(self,object_name):
        object_name.Start = object_name.Next_Start
    
    def init_step(self):
        field = list()
        field = map_proc.map_func.load_map('field.txt',field)
        for i in range(0,15):
            step_name = 'step_' + str(i) + '.txt'
            map_proc.map_func.write_map(step_name,field)
    
    def init_flag(self,object_name):
        object_name.flag = 0
    
    def init_goal(self):
        goal_num = input("please input number : ")
        goal_name = 'goal_' + goal_num + '.txt'
        self.Goal_field = list()
        map_proc.map_func.load_map(goal_name,self.Goal_field)