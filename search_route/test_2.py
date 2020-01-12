#coding utf-8

import route_proc
import map_proc
import goal_proc
import common_proc

this_device = 1

#デバイスの総数を設定
Common_data = common_proc.common_data(2,7,7)
#それぞれのデバイスを初期化
Device1 = route_proc.route_data(Common_data.H,Common_data.W,(3,4))
Device2 = route_proc.route_data(Common_data.H,Common_data.W,(3,3))
#Device_infoというリストにすべてのデバイスのオブジェクトを入れる
Device_info = [Device1,Device2]

while (int(input('please input 0(end) or 1(continue) : '))):
    #ゴールのマップを指定
    Common_data.init_goal()
    #それぞれのデバイスのゴールを設定する
    goal_proc.goal_func.search_goal(Common_data.ret_goal_field(),Device_info,Common_data.ret_dev_sum())
    #ループの外でstep_n.txtを初期化する
    Common_data.init_step()
    for i in range (Common_data.ret_dev_sum()):
        #ゴールのフィールドを設定
        Device_info[i].field = Common_data.Goal_field
        #デバイスのゴールを決定する
        map_proc.map_func.del_my_goal(Device_info[i])
        #デバイスのルートを策定する
        Device_info[i].search_route(Device_info[i],Device_info[i].field)
        #通る道を1で埋める
        Device_info[i].update_route()
        #ステップに書き込み
        map_proc.map_func.write_step(Device_info[i])
        if (i == this_device-1):
            #ルートを表示
            Device_info[i].show_route()
        #初期化
        Device_info[i].init_data(Common_data.H,Common_data.W)