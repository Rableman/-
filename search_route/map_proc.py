#coding utf-8

import copy

class map_func:
    #テキストから迷路の情報をリストとして読み込む
    def load_map(file_name,field_name):
        f = open(file_name,'r')
        for row in f:
            #改行文字を削除
            row = row.replace('\n', '')
            row_new = list()
            #文字から数値に変換
            for i in row:
                row_new.append(int(i))
            field_name.append(list(row_new))
        f.close()
        return field_name

    #リストの情報をファイルに書き込む
    def write_map(file_name,field_name):
        write_field = list()
        for row in field_name:
            #ファイル書き込み用にリストを変換
            row = str(row).replace(',','').replace('[','').replace(']','').replace(' ','')
            write_field.append(row)
        #1行ごとに改行文字を入れてファイルに書き込む
        f = open(file_name,'w')
        f.write('\n'.join(write_field))
        f.close()

    #全てのゴール地点が1で埋められているので、自分のゴール地点は0に置き換える
    def del_my_goal(object_name):
        x,y = object_name.Goal
        object_name.field[x][y] = 0
    
    #ユークリッド距離を計算    
    def cal_heuristic(start,goal):
        dis = ((goal[0]-start[0])**2+(goal[1]-start[1])**2)**0.5
        return dis

    #たどってきた経路の長さを計算
    def cal_distance(path):
        return len(path)

    def write_step(object_name):
        #初期位置以降の処理(ゴールの一個前まで)
        step_count = 1
        all_step = list() #全てのstepの情報を一時的に保持
        tmp_passed_list = copy.deepcopy(object_name.Passed_list)
        while len(tmp_passed_list) > 1:
            #step_n.txtのデータをfieldに格納する
            field = list()
            step_name = 'step_' + str(step_count) + '.txt'
            field = map_func.load_map(step_name,field)
            #次の位置を取り出す
            x,y = tmp_passed_list[1]
            #次に進む位置が0ならそのまま進む
            #1なら進まない ← 改善必要
            if (field[x][y] == 0):
                field[x][y] = 1
                tmp_passed_list.pop(0)
            else :
                #進むとぶつかる部分を通らないように、fieldを更新
                object_name.field[x][y] = 1
                return 1
            all_step.append(field)
            step_count += 1
        #ステップは最終的に書き込むようにする
        for i in range(step_count-1):
            #更新したマップを書き込む
            file_name = 'step_' + str(i+1) + '.txt'
            map_func.write_map(file_name,all_step[i])
        #ゴールにたどり着いたときの処理は必要ない
        #そもそもゴールは通らないようにしているため、step_n.txtで確認する必要なし
        return 0