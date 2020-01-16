#coding utf-8

<<<<<<< HEAD
from search_route import route_proc
from search_route import map_proc
from search_route import goal_proc
from search_route import common_proc
=======
>>>>>>> search

class route_main_func:
    #デバイスの総数、フィールドの座標数を設定
    def __init__(self):
        self.Device_sum = 3 #デバイスの総数
        self.H = 7 #H*Wのフィールド
        self.W = 7
        #それぞれのデバイスのインスタンスを作る
        self.Device1 = route_proc.route_data(self.H,self.W,(1,1))
        self.Device2 = route_proc.route_data(self.H,self.W,(1,2))
        self.Device3 = route_proc.route_data(self.H,self.W,(1,3))
        #Device_infoというリストにすべてのデバイスのインスタンスを入れる
        self.Device_info = [self.Device1,self.Device2,self.Device3]

    #デバイスが何番目なのかというローカル変数と3つのデバイスのスタート地点、ゴールのマップを引数
    # → 経路を返す
    def main(self,device_num,Device1_start,Device2_start,Device3_start,goal_map):
        goal = goal_map.split('\n')
        goal_map = []
        for row in goal:
            row_new = list()
            for i in row:
                row_new.append(int(i))
            goal_map.append(list(row_new))

        #それぞれのデバイスのスタート地点を更新
        common_proc.common_func.set_start(Device1_start,Device2_start,Device3_start,self.Device_info)
        #それぞれのデバイスのゴールを設定する
        goal_proc.goal_func.search_goal(goal_map,self.Device_info,self.Device_sum)
        #ループの外でstep_n.txtを初期化する
        common_proc.common_func.init_step()

        for i in range (self.Device_sum):
            #ゴールのフィールドをフィールドとして設定
            self.Device_info[i].field = copy.deepcopy(goal_map)
            #自分のデバイスの位置を削除
            map_proc.map_func.del_my_goal(self.Device_info[i])
            #デバイスのルートを策定する
            self.Device_info[i].search_route(self.Device_info[i],self.Device_info[i].field)
            #他のデバイスとぶつかった場合にはルートを決め直す
            while (map_proc.map_func.write_step(self.Device_info[i])):
                #初期化
                self.Device_info[i].init_data(self.H,self.W)
                #ルートを策定する
                self.Device_info[i].search_route(self.Device_info[i],self.Device_info[i].field)
            #通る道を1で埋める
            self.Device_info[i].update_route()
            if (i == device_num-1):
                #返すべきルートを保持
                return_route = self.Device_info[i].show_route()
                #返すべきゴールを代入
                return_goal = [self.Device_info[i].Goal[0],self.Device_info[i].Goal[1]]
            #デバッグ
            #self.Device_info[i].show_route_debug()
            #初期化
            self.Device_info[i].init_data(self.H,self.W)
        #探索したルートを返り値にする
        return return_goal,return_route
