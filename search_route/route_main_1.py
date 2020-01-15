#coding utf-8

import route_proc
import map_proc
import goal_proc
import common_proc

class route_main_func:
    #初期化の処理
    #引数にデバイスの総数、H*Wのフィールド、それぞれのデバイスのスタート地点を渡すと、
    #共通データとデバイス情報のリストを返す
    def init(device_sum,H,W,Device1_start):
        #デバイスの総数、フィールドの座標数を設定
        Common_data = common_proc.common_data(device_sum,H,W)
        #それぞれのデバイスを初期化
        Device1 = route_proc.route_data(Common_data.H,Common_data.W,Device1_start)
        #Device_infoというリストにすべてのデバイスのオブジェクトを入れる
        Device_info = [Device1]
        return Common_data,Device_info
    
    #引数にデバイスの総数とフィールドが入ったCommon_data,デバイスの情報リストのDevice_info,
    #どのデバイスなのか示すdevice_numを渡すと経路を出力
    def main(Common_data,Device_info,device_num,goal_map):
        #ゴールのマップを指定
        Common_data.init_goal(goal_map)
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
            if (i == device_num-1):
                #ルートを表示
                Device_info[i].show_route()
            #初期化
            Device_info[i].init_data(Common_data.H,Common_data.W)