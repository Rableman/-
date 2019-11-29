#coding utf-8

def cal_distance(start,goal):
    #ユークリッド距離(平方根は取らない)を計算
    dis = (goal[0]-start[0])**2+(goal[1]-start[1])**2
    return dis

def set_device(x,y):
    #一番ゴール(x,y)からの距離が近いデバイスを選定してそのデバイスのゴールとフラグを書き換える
    min_dev_num = 100
    for j in range(1):
        dis = cal_distance((1,1),(x,y)) #それぞれのデバイスのスタート位置に第一引数を書き換える
        if dis < min_dev_num : #and device_info[j].flag == 0かの確認
            min_dev_num = dis
            dev_num = j
    #device_info[j].goalを(1,i)に書き換える
    #device_info[j].flagを1にする
    print(min_dev_num,dev_num)

def search_goal(goal_field):
    #外の枠から順番にゴール地点がないかを確認していく
    for i in range(1,6):
        if goal_field[1][i] == 1: #ゴールが見つかる
            set_device(1,i)
    if goal_field[2][1] == 1:
        set_device(2,1)
    if goal_field[2][5] == 1:
        set_device(2,5)
    if goal_field[3][1] == 1:
        set_device(3,1)
    if goal_field[3][5] == 1:
        set_device(3,5)
    if goal_field[4][1] == 1:
        set_device(4,1)
    if goal_field[4][5] == 1:
        set_device(4,5)
    for i in range (1,6):
        if goal_field[5][i] == 1:
            set_device(5,i)
    for i in range (2,5):
        if goal_field[2][i] == 1:
            set_device(2,i)
    if goal_field[3][2] == 1:
        set_device(3,2)
    if goal_field[3][4] == 1:
        set_device(3,4)
    for i in range (2,5):
        if goal_field[4][i] == 1:
            set_device(4,i)
    if goal_field[3][3] == 1:
        set_device(3,3)

'''
def load_map(goal,file_name):
    #迷路の情報をfieldにリストで格納
    f = open(file_name,'r')
    for row in f:
        row_re = row.replace('\n', '')
        row_new = list()
        for i in row_re: #文字から数値に変換
            row_new.append(int(i))
        goal.append(list(row_new))
    f.close()            
'''

goal_field = list()
load_map(goal_field,'goal_1.txt')
search_goal(goal_field)