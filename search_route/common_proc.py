#coding utf-8
import map_proc

class common_data:
    def __init__(self,device_num,h,w):
        self.Device_sum = device_num #デバイスの総数
        self.Goal_field = list() #ゴールのフィールド
        self.H = h #H*Wのフィールド
        self.W = w
    
    #デバイスの総数を返す
    def ret_dev_sum(self):
        return self.Device_sum
    
    #ゴールのフィールドを返す
    def ret_goal_field(self):
        return self.Goal_field
        
    #次のスタート位置を書き換える
    def set_start(self,object_name):
        object_name.Start = object_name.Next_Start
    
    #step_n.txtを初期化する
    def init_step(self):
        field = list()
        field = map_proc.map_func.load_map('field.txt',field)
        #step0~14.txtをfield.txtと同様にすることで初期化
        for i in range(0,15):
            step_name = 'step_' + str(i) + '.txt'
            map_proc.map_func.write_map(step_name,field)
    
    #ゴールの位置を変更する
    def init_goal(self):
        #ユーザの入力でゴールのフィールドを選択する
        goal_num = input("please input number : ")
        goal_name = 'goal_' + goal_num + '.txt'
        #ゴールのフィールドを初期化
        self.Goal_field = list()
        #ゴールのフィールドを読み込む
        map_proc.map_func.load_map(goal_name,self.Goal_field)