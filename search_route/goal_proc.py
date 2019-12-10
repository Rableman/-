#coding utf-8

import map_proc

class goal_func:
    def cal_distance(start,goal):
        #ユークリッド距離(平方根は取らない)を計算
        dis = (goal[0]-start[0])**2+(goal[1]-start[1])**2
        return dis

    def set_device(x,y,object_name):
        #一番ゴール(x,y)からの距離が近いデバイスを選定してそのデバイスのゴールとフラグを書き換える
        min_dev_num = 100
        for i in range(2):
            dis = goal_func.cal_distance(object_name[i].Start,(x,y)) #それぞれのデバイスのスタート位置に第一引数を書き換える
            if dis < min_dev_num and object_name[i].flag == 0 :
                min_dev_num = dis
                dev_num = i
        object_name[dev_num].Goal = (x,y)
        object_name[dev_num].flag = 1
        #print(min_dev_num,dev_num,object_name[dev_num].Goal) #デバッグ

    def search_goal(goal_field,object_name):
        #外の枠から順番にゴール地点がないかを確認していく
        for i in range(1,6):
            if goal_field[1][i] == 1: #ゴールが見つかる
                goal_func.set_device(1,i,object_name)
        if goal_field[2][1] == 1:
            goal_func.set_device(2,1,object_name)
        if goal_field[2][5] == 1:
            goal_func.set_device(2,5,object_name)
        if goal_field[3][1] == 1:
            goal_func.set_device(3,1,object_name)
        if goal_field[3][5] == 1:
            goal_func.set_device(3,5,object_name)
        if goal_field[4][1] == 1:
            goal_func.set_device(4,1,object_name)
        if goal_field[4][5] == 1:
            goal_func.set_device(4,5,object_name)
        for i in range (1,6):
            if goal_field[5][i] == 1:
                goal_func.set_device(5,i,object_name)
        for i in range (2,5):
            if goal_field[2][i] == 1:
                goal_func.set_device(2,i,object_name)
        if goal_field[3][2] == 1:
            goal_func.set_device(3,2,object_name)
        if goal_field[3][4] == 1:
            goal_func.set_device(3,4,object_name)
        for i in range (2,5):
            if goal_field[4][i] == 1:
                goal_func.set_device(4,i,object_name)
        if goal_field[3][3] == 1:
            goal_func.set_device(3,3,object_name)