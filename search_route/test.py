#coding utf-8

import route_proc
import map_proc
import goal_proc



goal_field = list()
map_proc.map_func.load_map('goal_1.txt',goal_field)
Device1 = route_proc.route_data(7,7,(4,1))
#Device2 = route_proc.route_data(7,7,(5,4))
Device_info = [Device1] #Device_infoというリストにすべてのデバイスのオブジェクトを入れる
goal_proc.goal_func.search_goal(goal_field,Device_info,1)

for i in range (1):
    Device_info[i].route.append(Device_info[i].Goal)
    map_proc.map_func.load_map('field.txt',Device_info[i].field)
    Device_info[i].search_route('field.txt',Device_info[i],Device_info[i].field)
    Device_info[i].update_route()
    Device_info[i].show_route()
