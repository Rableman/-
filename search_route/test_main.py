#coding utf-8

import route_main
import map_proc
import common_proc

#ローカル変数
device_num = 3
#route_mainをオブジェクト化
Route_main = route_main.route_main_func()

#この部分がサーバーからゴールのリストが送信される所に変わる
goal_map = list()
map_proc.map_func.load_map(common_proc.common_func.select_goal(),goal_map)

#デバイスが何番目なのかというローカル変数と3つのデバイスのスタート地点、ゴールのマップを引数 → 経路を返す
goal,a = Route_main.main(device_num,(1,1),(2,2),(5,3),goal_map)
print(goal)
print(a)


#この部分がサーバーからゴールのリストが送信される所に変わる
goal_map = list()
map_proc.map_func.load_map(common_proc.common_func.select_goal(),goal_map)

#デバイスが何番目なのかというローカル変数と3つのデバイスのスタート地点、ゴールのマップを引数 → 経路を返す
goal,a = Route_main.main(device_num,(2,1),(1,2),(1,3),goal_map)
print(goal)
print(a)
