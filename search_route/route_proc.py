#coding: utf-8
import heapq
import sys
import random
import map_proc
import numpy as np

class route_data:
    def __init__(self,h,w,start):
        self.H = h #縦幅H*横幅Wのグリッド
        self.W = w
        self.field = list() #グリッド上の情報を格納 自分以外のゴールと壁を1とする
        self.Route_Field = np.zeros((self.H,self.W),dtype=int) #最終経路の表示に使用
        self.CL = np.zeros((self.H,self.W), dtype=int) #CLは2次元配列で用意
        self.OL = list() #OLはリストを用いて実装
        self.Cost = np.zeros((self.H,self.W), dtype=int) + 999 #経路を辿るためのコスト
        self.Start = start #Start位置はあらかじめタプル型で用意
        self.flag = 0 #フラグが0のときはゴールが割り振られていない 1のときはゴールが割り振られている
        self.route = list() #自分の道順はここに格納される
        
        self.OL_can = list() #next()内での候補の格納に使用
        self.passed_list = [start] #探索した座標リスト

    def next(self,x):
        #行名がy軸 列名がx軸に対応しているため、(x[1],x[0])の座標となる
        #上に進めるか判定
        if(self.field[x[1]-1][x[0]]==0 and self.CL[x[1]-1][x[0]]==0):
            #self.OL.append((x[0],x[1]-1))
            self.OL_can.append((x[0],x[1]-1))
            self.Cost[x[1]-1][x[0]] = self.Cost[x[1]][x[0]] + 1 
            #print('上')
        #下に進めるか判定
        if(self.field[x[1]+1][x[0]]==0 and self.CL[x[1]+1][x[0]]==0):
            #self.OL.append((x[0],x[1]+1))
            self.OL_can.append((x[0],x[1]+1))
            self.Cost[x[1]+1][x[0]] = self.Cost[x[1]][x[0]] + 1
            #print('下')
        #右に進めるか判定
        if(self.field[x[1]][x[0]+1]==0 and self.CL[x[1]][x[0]+1]==0):
            #self.OL.append((x[0]+1,x[1]))
            self.OL_can.append((x[0]+1,x[1]))
            self.Cost[x[1]][x[0]+1] = self.Cost[x[1]][x[0]] + 1
            #print('右')
        #左に進めるか判定
        if(self.field[x[1]][x[0]-1]==0 and self.CL[x[1]][x[0]-1]==0):
            #self.OL.append((x[0]-1,x[1]))
            self.OL_can.append((x[0]-1,x[1]))
            self.Cost[x[1]][x[0]-1] = self.Cost[x[1]][x[0]] + 1
            #print('左')
        return
    '''
    def format_OL(self):
        self.OL.append(self.Start) #OLに初期状態を追加
        self.Cost[self.Start[1]][self.Start[0]] = 0
    '''

    #heapqを使ってA*アルゴリズムを実装する
    def search_route(self,file_name,object_name,var_name):
        #初期スコアを計算
        start_score = map_proc.map_func.cal_distance(self.passed_list) + map_proc.map_func.cal_heuristic(self.Start,self.Goal)
        #探索済み座標とその座標にたどり着いた経路のスコアを格納
        checked = {self.Start: start_score}
        #探索ヒープに経路リストを格納
        heapq.heappush(self.OL,(start_score,self.passed_list))
        #while文で探索する
        while len(self.OL) > 0:
            score, self.passed_list = heapq.heappop(self.OL)
            #xは現在探索している座標
            x = self.passed_list[-1]
            self.CL[x[1]][x[0]] = 1
            #Goalについた時の判定
            if(x == self.Goal):
                print(self.passed_list)
                break
            object_name.next(x)
            for pos in self.OL_can:
                new_passed_list = self.passed_list + [pos]
                pos_score = map_proc.map_func.cal_distance(new_passed_list) + map_proc.map_func.cal_heuristic(pos,self.Goal)
                if pos in checked and checked[pos] <= pos_score:
                    continue
                checked[pos] = pos_score
                heapq.heappush(self.OL,(pos_score,new_passed_list))
        if(x!=self.Goal):
            print("Fault\n")
            sys.exit()

#reverse_routeも終わらない
    def reverse_route(self):
        # ゴールから逆順でルート計算
        point_now = self.Goal
        cost_now = self.Cost[self.Goal[0], self.Goal[1]]
        while cost_now > 0:
            #上から来た場合
            try:
                if self.Cost[point_now[1] - 1][ point_now[0]] == cost_now - 1:
                    #更新
                    point_now = (point_now[0], point_now[1]-1)
                    cost_now = cost_now - 1
                    #記録
                    self.route.append(point_now)
            except: pass
            #下から来た場合
            try:
                if self.Cost[point_now[1] + 1, point_now[0]] == cost_now - 1:
                    #更新
                    point_now = (point_now[0], point_now[1]+1)
                    cost_now = cost_now - 1
                    #記録
                    self.route.append(point_now)
            except: pass
            #左から来た場合    
            try:
                if self.Cost[point_now[1], point_now[0] - 1] == cost_now - 1:
                    #更新
                    point_now = (point_now[0]-1, point_now[1])
                    cost_now = cost_now - 1
                    #記録
                    self.route.append(point_now)
            except: pass
            #右から来た場合
            try:
                if self.Cost[point_now[1], point_now[0] + 1] == cost_now - 1:
                    #更新
                    point_now = (point_now[0]+1, point_now[1])
                    cost_now = cost_now - 1
                    #記録
                    self.route.append(point_now)
            except: pass
        #ルートを逆順にする
        self.route = self.route[::-1]
        print(self.route)

    def update_route(self):
        #通る経路を1で埋める
        #for route_i in self.route:
        for route_i in self.passed_list:
            self.Route_Field[route_i[0]][route_i[1]] = 1

    def show_route(self):
        #探索したルートを表示
        for i in self.Route_Field:
            print(*i)