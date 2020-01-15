#coding utf-8

import route_proc
import map_proc
import goal_proc
import common_proc
import route_main_1

#ローカル変数
device_num = 1

#この部分がサーバーからゴールのリストが送信される所に変わる
goal_map = list()
map_proc.map_func.load_map('goal_1.txt',goal_map)

#初期化の処理。引数にデバイスの総数、H*Wのフィールド、それぞれのデバイスのスタート地点を渡すと、共通データとデバイス情報のリストを返す
Common_data,Device_info = route_main_1.route_main_func.init(1,7,7,(1,1))

#引数にデバイスの総数とフィールドが入ったCommon_data,デバイスの情報リストのDevice_info,どのデバイスなのか示すdevice_numを渡すと経路が出力
route_main_1.route_main_func.main(Common_data,Device_info,device_num,goal_map)