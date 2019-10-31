#coding: utf-8
import queue
import sys
import numpy as np

H = 11 #N*Mのグリッド
W = 11
field = list() #グリッド上の情報を格納
Route_Field = np.zeros((H,W),dtype=int) #最終経路の表示に使用
CL = np.zeros((H,W), dtype=int) #CLは2次元配列で用意
OL = queue.Queue() #キューはモジュールを用いる
Cost = np.zeros((H,W), dtype=int) + 999 #経路を辿るためのコスト
Start = (1,1) #Start位置とGoal位置はあらかじめタプル型で用意
Goal = (9,9)

def next(x):
    #上に進めるか判定
    if(field[x[1]-1][x[0]]==0 and CL[x[1]-1][x[0]]==0):
        OL.put((x[0],x[1]-1))
        Cost[x[1]-1][x[0]] = Cost[x[1]][x[0]] + 1 
    #下に進めるか判定
    if(field[x[1]+1][x[0]]==0 and CL[x[1]+1][x[0]]==0):
        OL.put((x[0],x[1]+1))
        Cost[x[1]+1][x[0]] = Cost[x[1]][x[0]] + 1
    #右に進めるか判定
    if(field[x[1]][x[0]+1]==0 and CL[x[1]][x[0]+1]==0):
        OL.put((x[0]+1,x[1]))
        Cost[x[1]][x[0]+1] = Cost[x[1]][x[0]] + 1
    #左に進めるか判定
    if(field[x[1]][x[0]-1]==0 and CL[x[1]][x[0]-1]==0):
        OL.put((x[0]-1,x[1]))
        Cost[x[1]][x[0]-1] = Cost[x[1]][x[0]] + 1
    return

#迷路の情報をfieldにリストで格納
f = open('field.txt','r')
for row in f:
    row_re = row.replace('\n', '')
    row_new = list()
    for i in row_re: #文字から数値に変換
        row_new.append(int(i))
    field.append(list(row_new))
f.close()

OL.put(Start) #OLに初期状態を追加
Cost[Start[1]][Start[0]] = 0

#while文で探索する
while not OL.empty():
    x=OL.get()
    CL[x[1]][x[0]]=1
    #Goalについた時の判定
    if(x == Goal):
        break
    next(x)

if(x!=Goal):
    print("Fault\n")
    sys.exit()

# ゴールから逆順でルート計算
point_now = Goal
cost_now = Cost[Goal[0], Goal[1]]
route = [Goal]
while cost_now > 0:
    #上から来た場合
    try:
        if Cost[point_now[0] - 1][ point_now[1]] == cost_now - 1:
            #更新
            point_now = (point_now[0] - 1, point_now[1])
            cost_now = cost_now - 1
            #記録
            route.append(point_now)
    except: pass
    #下から来た場合
    try:
        if Cost[point_now[0] + 1, point_now[1]] == cost_now - 1:
            #更新
            point_now = (point_now[0] + 1, point_now[1])
            cost_now = cost_now - 1
            #記録
            route.append(point_now)
    except: pass
    #左から来た場合    
    try:
        if Cost[point_now[0], point_now[1] - 1] == cost_now - 1:
            #更新
            point_now = (point_now[0], point_now[1] - 1)
            cost_now = cost_now - 1
            #記録
            route.append(point_now)
    except: pass
    #右から来た場合
    try:
        if Cost[point_now[0], point_now[1] + 1] == cost_now - 1:
            #更新
            point_now = (point_now[0], point_now[1] + 1)
            cost_now = cost_now - 1
            #記録
            route.append(point_now)
    except: pass

#ルートを逆順にする
route = route[::-1]

for route_i in route:
    Route_Field[route_i[0]][route_i[1]] = 1

for i in Route_Field:
    print(*i)