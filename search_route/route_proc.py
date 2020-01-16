#coding: utf-8
import heapq
import sys
import random
import map_proc
import numpy as np

class route_data:
    def __init__(self,h,w,start):
        self.field = list() #グリッド上の情報を格納 自分以外のゴールと壁を1とする
        self.Route_Field = np.zeros((h,w),dtype=int) #最終経路の表示に使用
        self.CL = np.zeros((h,w), dtype=int) #CLは2次元配列で用意
        self.OL = list() #OLはリストを用いて実装
        self.OL_can = list() #next()内での候補の格納に使用
        self.Start = start #Start位置はあらかじめタプル型で用意
        self.Goal = (0,0) #Goal位置はタプル型で用意
        self.flag = 0 #フラグが0のときはゴールが割り振られていない 1のときはゴールが割り振られている
        self.Passed_list = [self.Start] #探索した座標リスト(このリストが最終的に経路となる)
    
    #初期化の処理
    def init_data(self,h,w):
        self.flag = 0
        self.Route_Field = np.zeros((h,w),dtype=int)
        self.CL = np.zeros((h,w), dtype=int)
        self.OL = list()
        self.OL_can = list()

    #x座標の上下左右のうち進める部分を探索する
    def next(self,x):
        #上に進めるか判定
        if(self.field[x[0]-1][x[1]]==0 and self.CL[x[0]-1][x[1]]==0):
            self.OL_can.append((x[0]-1,x[1]))
        #下に進めるか判定
        if(self.field[x[0]+1][x[1]]==0 and self.CL[x[0]+1][x[1]]==0):
            self.OL_can.append((x[0]+1,x[1]))
        #右に進めるか判定
        if(self.field[x[0]][x[1]+1]==0 and self.CL[x[0]][x[1]+1]==0):
            self.OL_can.append((x[0],x[1]+1))
        #左に進めるか判定
        if(self.field[x[0]][x[1]-1]==0 and self.CL[x[0]][x[1]-1]==0):
            self.OL_can.append((x[0],x[1]-1))
        return

    #heapq(優先度キュー)を使ってA*アルゴリズムを実装し、経路探索を行う
    def search_route(self,object_name,var_name):
        #初期化
        self.Passed_list = [self.Start]
        #初期スコアを計算
        start_score = map_proc.map_func.cal_distance(self.Passed_list) + map_proc.map_func.cal_heuristic(self.Start,self.Goal)
        #探索済み座標とその座標にたどり着いた経路のスコアを格納
        checked = {self.Start: start_score}
        #探索ヒープに経路リストを格納
        heapq.heappush(self.OL,(start_score,self.Passed_list))
        #while文で探索する
        while len(self.OL) > 0:
            score, self.Passed_list = heapq.heappop(self.OL)
            #xは現在探索している座標
            x = self.Passed_list[-1]
            self.CL[x[1]][x[0]] = 1
            #Goalについた時の判定
            if(x == self.Goal):
                break
            #4方向について探索
            object_name.next(x)
            #探索可能な方向についてスコアを計算
            for pos in self.OL_can:
                #経路リストに探索中の座標を追加した候補リストを作成
                new_passed_list = self.Passed_list + [pos]
                #候補のリストのスコアを計算
                pos_score = map_proc.map_func.cal_distance(new_passed_list) + map_proc.map_func.cal_heuristic(pos,self.Goal)
                #探索中の座標が他の経路で探索済みか確認
                #探索済みの場合は、前回のスコアと今回のスコアを比較
                #今回のスコアのほうが大きい場合、次の方角の座標の探索へ
                if pos in checked and checked[pos] <= pos_score:
                    continue
                #今回のスコアのほうが小さい場合、チェック済みリストに格納
                checked[pos] = pos_score
                #探索ヒープに経路リストを格納
                heapq.heappush(self.OL,(pos_score,new_passed_list))
            self.OL_can = list()
        #探索失敗時
        if(x!=self.Goal):
            #print("Fault\n")
            sys.exit()

    #通る経路を1で埋める
    def update_route(self):
        for route_i in self.Passed_list:
            self.Route_Field[route_i[0]][route_i[1]] = 1

    #探索したルートを返り値にする
    def show_route(self):
        show_field = list()
        for row in self.Route_Field:
            #出力用にリストを変換
            row = str(row).replace(',','').replace('[','').replace(']','').replace(' ','')
            show_field.append(row)
        show_field = '\n'.join(show_field)
        return show_field
    
    def show_route_debug(self):
        print(self.Passed_list)
        for i in self.Route_Field:
            print(*i)
        print('')