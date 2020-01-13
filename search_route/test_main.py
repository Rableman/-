#coding utf-8

import route_proc
import map_proc
import common_proc
import route_main

#ローカル変数
device_num = 1
#route_mainをオブジェクト化
Route_main = route_main.route_main_func()

#この部分がサーバーからゴールのリストが送信される所に変わる
goal_map = list()
map_proc.map_func.load_map(common_proc.common_func.select_goal(),goal_map)

#デバイスが何番目なのかというローカル変数と3つのデバイスのスタート地点、ゴールのマップを引数 → 経路を返す
a = Route_main.main(device_num,(1,1),(1,2),(1,3),goal_map)
print(a)

#この部分がサーバーからゴールのリストが送信される所に変わる
goal_map = list()
map_proc.map_func.load_map(common_proc.common_func.select_goal(),goal_map)

#デバイスが何番目なのかというローカル変数と3つのデバイスのスタート地点、ゴールのマップを引数 → 経路を返す
a = Route_main.main(device_num,(2,1),(1,2),(1,3),goal_map)
print(a)





'''
#この部分がサーバーからゴールのリストが送信される所に変わる
goal_map = list()
map_proc.map_func.load_map(common_proc.common_data.select_goal(),goal_map)

#初期化の処理。引数にデバイスの総数、H*Wのフィールド、それぞれのデバイスのスタート地点を渡すと、共通データとデバイス情報のリストを返す
Common_data,Device_info = route_main.route_main_func.init(3,7,7,(3,4),(3,3),(1,1))

#引数にデバイスの総数とフィールドが入ったCommon_data,デバイスの情報リストのDevice_info,どのデバイスなのか示すdevice_numを渡すと経路が出力
route_main.route_main_func.main(Common_data,Device_info,device_num,goal_map)
'''