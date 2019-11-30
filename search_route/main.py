#coding utf-8

import route_proc
import map_proc

Device1 = route_proc.route_data(7,7,(1,1))
Device1.Goal = (4,4)
Device1.route = [Device1.Goal]
Device_info = [Device1] #Device_infoというリストにすべてのデバイスのオブジェクトを入れる
map_proc.map_func.load_map('field.txt',Device_info[0].field)
Device_info[0].format_OL()
Device_info[0].search_route('field.txt',Device_info[0],Device_info[0].field)
Device_info[0].reverse_route()
Device_info[0].update_route()
Device_info[0].show_route()