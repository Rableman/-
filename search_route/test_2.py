#coding utf-8

import route_proc
import map_proc
import goal_proc
import common_proc

Common_data = common_proc.common_data(2)
map_proc.map_func.load_map('goal_2.txt',Common_data.Goal_field)
Device1 = route_proc.route_data(7,7,(1,2))
Device2 = route_proc.route_data(7,7,(5,4))
Device_info = [Device1,Device2] #Device_infoというリストにすべてのデバイスのオブジェクトを入れる
goal_proc.goal_func.search_goal(Common_data.ret_goal_field(),Device_info,Common_data.ret_dev_sum())

#ループ分の外でstep_n.txtを初期化する
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
    #初期位置をゴールに初期化
    Common_data.set_start(Device_info[i])
    #ステップに書き込み
    map_proc.map_func.write_step(Device_info[i])
    #ルートを表示
    Device_info[i].show_route()