#coding utf-8

import route_proc
import map_proc
import goal_proc
import common_proc

Common_data = common_proc.common_data(1)
map_proc.map_func.load_map('goal_1.txt',Common_data.Goal_field)
Device1 = route_proc.route_data(7,7,(4,1))
#Device_infoというリストにすべてのデバイスのオブジェクトを入れる
Device_info = [Device1]
goal_proc.goal_func.search_goal(Common_data.ret_goal_field(),Device_info,Common_data.ret_dev_sum())

for i in range (Common_data.ret_dev_sum()):
    map_proc.map_func.load_map('field.txt',Device_info[i].field)
    Device_info[i].search_route('field.txt',Device_info[i],Device_info[i].field)
    Device_info[i].update_route()
    Device_info[i].show_route()
