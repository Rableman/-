#coding utf-8

import map_proc

class goal_func:
    def set_device(x,y,object_name,dev_sum):
        #一番ゴール(x,y)からの距離が近いデバイスを選定してそのデバイスのゴールとフラグを書き換える
        min_dev_num = 100
        for i in range(dev_sum):
            #それぞれのデバイスのスタート位置からゴールまでの距離を計算
            dis = map_proc.map_func.cal_heuristic(object_name[i].Start,(x,y))
            #計算したデバイスの距離が最小だった場合、デバイスの番号を記録
            if dis < min_dev_num and object_name[i].flag == 0 :
                min_dev_num = dis
                dev_num = i
        #距離が一番近いデバイスのゴール、フラグ、次のスタート位置を記録
        object_name[dev_num].Goal = (x,y)
        object_name[dev_num].flag = 1
        object_name[dev_num].Next_Start = (x,y)

    def search_goal(goal_field,object_name,dev_sum):
        #外の枠から順番にゴール地点がないかを確認していく
        for i in range(1,6):
            if goal_field[1][i] == 1: #ゴールが見つかる
                goal_func.set_device(1,i,object_name,dev_sum)
        if goal_field[2][1] == 1:
            goal_func.set_device(2,1,object_name,dev_sum)
        if goal_field[2][5] == 1:
            goal_func.set_device(2,5,object_name,dev_sum)
        if goal_field[3][1] == 1:
            goal_func.set_device(3,1,object_name,dev_sum)
        if goal_field[3][5] == 1:
            goal_func.set_device(3,5,object_name,dev_sum)
        if goal_field[4][1] == 1:
            goal_func.set_device(4,1,object_name,dev_sum)
        if goal_field[4][5] == 1:
            goal_func.set_device(4,5,object_name,dev_sum)
        for i in range (1,6):
            if goal_field[5][i] == 1:
                goal_func.set_device(5,i,object_name,dev_sum)
        for i in range (2,5):
            if goal_field[2][i] == 1:
                goal_func.set_device(2,i,object_name,dev_sum)
        if goal_field[3][2] == 1:
            goal_func.set_device(3,2,object_name,dev_sum)
        if goal_field[3][4] == 1:
            goal_func.set_device(3,4,object_name,dev_sum)
        for i in range (2,5):
            if goal_field[4][i] == 1:
                goal_func.set_device(4,i,object_name,dev_sum)
        if goal_field[3][3] == 1:
            goal_func.set_device(3,3,object_name,dev_sum)