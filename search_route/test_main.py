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

for i in range (Common_data.ret_dev_sum()):
    map_proc.map_func.load_map('field.txt',Device_info[i].field)
    Device_info[i].search_route('field.txt',Device_info[i],Device_info[i].field)
    Device_info[i].update_route()
    Device_info[i].show_route()