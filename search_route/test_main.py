#coding utf-8

import route_proc
import map_proc
import goal_proc

goal_field = list()
map_proc.map_func.load_map('goal_2.txt',goal_field)
Device1 = route_proc.route_data(7,7,(1,2))
Device2 = route_proc.route_data(7,7,(5,4))
Device_info = [Device1,Device2] #Device_infoというリストにすべてのデバイスのオブジェクトを入れる
goal_proc.goal_func.search_goal(goal_field,Device_info)

for i in range (2):
    Device_info[i].route.append(Device_info[i].Goal)
    map_proc.map_func.load_map('field.txt',Device_info[i].field)
    Device_info[i].format_OL()
    Device_info[i].search_route('field.txt',Device_info[i],Device_info[i].field)
    Device_info[i].reverse_route()
    Device_info[i].update_route()
    Device_info[i].show_route()
