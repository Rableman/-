#coding utf-8
from search_route import map_proc
import os

class common_func:
    #step_n.txtを初期化する
    def init_step():
        field = list()
        field = map_proc.map_func.load_map('field.txt',field)
        #step0~14.txtをfield.txtと同様にすることで初期化
        for i in range(1,15):
            step_name = 'step_' + str(i) + '.txt'
            map_proc.map_func.write_map(step_name,field)
    
    #step_n.txtを削除
    def del_step():
        for i in range(1,15):
            step_name = 'step_' + str(i) + '.txt'
            os.remove(step_name)
    
    #ゴールのマップを選ぶ(デバッグ用)
    def select_goal():
        #ユーザの入力でゴールのフィールドを選択する(ランダムなどに変更可能)
        goal_num = input()
        goal_name = 'goal_' + goal_num + '.txt'
        return goal_name
    
    #スタート地点の設定
    def set_start(Device1_start,Device2_start,Device3_start,Device_info):
        Device_info[0].Start = Device1_start
        Device_info[1].Start = Device2_start
        Device_info[2].Start = Device3_start