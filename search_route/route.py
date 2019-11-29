#coding: utf-8
import queue
import sys
import random
import random_setup
#import goal_setup
import numpy as np

class route_data:
    def __init__(self,h,w,start):
        self.H = h #N*Mのグリッド
        self.W = w
        self.field = list() #グリッド上の情報を格納
        self.Route_Field = np.zeros((self.H,self.W),dtype=int) #最終経路の表示に使用
        self.CL = np.zeros((self.H,self.W), dtype=int) #CLは2次元配列で用意
        self.OL = queue.Queue() #キューはモジュールを用いる
        self.Cost = np.zeros((self.H,self.W), dtype=int) + 999 #経路を辿るためのコスト
        self.Start = start #Start位置とGoal位置はあらかじめタプル型で用意
        #self.Goal
        #self.route = [self.Goal]

    def next(self,x):
        #上に進めるか判定
        if(self.field[x[1]-1][x[0]]==0 and self.CL[x[1]-1][x[0]]==0):
            self.OL.put((x[0],x[1]-1))
            self.Cost[x[1]-1][x[0]] = self.Cost[x[1]][x[0]] + 1 
        #下に進めるか判定
        if(self.field[x[1]+1][x[0]]==0 and self.CL[x[1]+1][x[0]]==0):
            self.OL.put((x[0],x[1]+1))
            self.Cost[x[1]+1][x[0]] = self.Cost[x[1]][x[0]] + 1
        #右に進めるか判定
        if(self.field[x[1]][x[0]+1]==0 and self.CL[x[1]][x[0]+1]==0):
            self.OL.put((x[0]+1,x[1]))
            self.Cost[x[1]][x[0]+1] = self.Cost[x[1]][x[0]] + 1
        #左に進めるか判定
        if(self.field[x[1]][x[0]-1]==0 and self.CL[x[1]][x[0]-1]==0):
            self.OL.put((x[0]-1,x[1]))
            self.Cost[x[1]][x[0]-1] = self.Cost[x[1]][x[0]] + 1
        return

    def load_map(self,file_name,var_name):
        #迷路の情報をfieldにリストで格納
        f = open(file_name,'r')
        for row in f:
            row_re = row.replace('\n', '')
            row_new = list()
            for i in row_re: #文字から数値に変換
                row_new.append(int(i))
            #self.var_name.append(list(row_new))
            var_name.append(list(row_new))
        f.close()

    '''
    def write_map(self,file_name):
        device = random_setup.rand_map(1,5) #今度ランダムじゃないものに置き換える？
        self.field[device[0]][device[1]] = 1

    def  update_map(self,file_name,object_name,var_name):
        self.field = list()
        object_name.load_map(file_name,var_name)
        for i in range(8):
            object_name.write_map(file_name)
    '''

    def format_OL(self):
        self.OL.put(self.Start) #OLに初期状態を追加
        self.Cost[self.Start[1]][self.Start[0]] = 0

    def search_route(self,file_name,object_name,var_name):
        #while文で探索する
        while not self.OL.empty():
            #object_name.update_map(file_name,object_name,var_name)
            x = self.OL.get()
            self.CL[x[1]][x[0]]=1
            #Goalについた時の判定
            if(x == self.Goal):
                break
            object_name.next(x)
        if(x!=self.Goal):
            print(self.Goal)
            print("Fault\n")
            sys.exit()

    def reverse_route(self):
        # ゴールから逆順でルート計算
        point_now = self.Goal
        cost_now = self.Cost[self.Goal[0], self.Goal[1]]
        while cost_now > 0:
            #上から来た場合
            try:
                if self.Cost[point_now[0] - 1][ point_now[1]] == cost_now - 1:
                    #更新
                    point_now = (point_now[0] - 1, point_now[1])
                    cost_now = cost_now - 1
                    #記録
                    self.route.append(point_now)
            except: pass
            #下から来た場合
            try:
                if self.Cost[point_now[0] + 1, point_now[1]] == cost_now - 1:
                    #更新
                    point_now = (point_now[0] + 1, point_now[1])
                    cost_now = cost_now - 1
                    #記録
                    self.route.append(point_now)
            except: pass
            #左から来た場合    
            try:
                if self.Cost[point_now[0], point_now[1] - 1] == cost_now - 1:
                    #更新
                    point_now = (point_now[0], point_now[1] - 1)
                    cost_now = cost_now - 1
                    #記録
                    self.route.append(point_now)
            except: pass
            #右から来た場合
            try:
                if self.Cost[point_now[0], point_now[1] + 1] == cost_now - 1:
                    #更新
                    point_now = (point_now[0], point_now[1] + 1)
                    cost_now = cost_now - 1
                    #記録
                    self.route.append(point_now)
            except: pass
        #ルートを逆順にする
        self.route = self.route[::-1]
        print(self.route)

    def update_route(self):
        #通る経路を1で埋める
        for route_i in self.route:
            self.Route_Field[route_i[0]][route_i[1]] = 1

    def show_route(self):
        #探索したルートを表示
        for i in self.Route_Field:
            print(*i)
    '''
    def show_now_map(self,file_name,object_name,var_name):
        object_name.load_map(file_name,var_name)
    '''
'''
Device1 = route_data(7,7,(1,1))
Device1.Goal = (4,4)
Device1.route = [Device1.Goal]
Device_info = [Device1] #Device_infoというリストにすべてのデバイスのオブジェクトを入れる
Device_info[0].load_map('field.txt',Device_info[0].field)
Device_info[0].format_OL()
Device_info[0].search_route('field.txt',Device_info[0],Device_info[0].field)
Device_info[0].reverse_route()
Device_info[0].update_route()
Device_info[0].show_route()
'''