#coding utf-8

class map_func:
    #迷路の情報をfield_nameにリストで格納
    def load_map(file_name,field_name):
        f = open(file_name,'r')
        for row in f:
            row_re = row.replace('\n', '')
            row_new = list()
            #文字から数値に変換
            for i in row_re:
                row_new.append(int(i))
            field_name.append(list(row_new))
        f.close()
        return field_name

    def write_map(file_name,field_name):
        write_field = list()
        for row in field_name:
            row_new = str(row).replace(',','').replace('[','').replace(']','').replace(' ','')
            write_field.append(row_new)
        f = open(file_name,'w')
        f.write('\n'.join(write_field))
        f.close()

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
        #step_0.txtのデータをfieldに格納する
        field = list()
        step_name = 'step_0.txt'
        field = map_func.load_map(step_name,field)
        #初期位置を取り出す
        x,y = object_name.Passed_list[0]
        #フィールドの初期位置を1で埋める
        field[x][y] = 1
        #更新したマップを書き込む
        file_name = 'step_0.txt'
        map_func.write_map(file_name,field)
        
        #初期位置以降の処理(ゴールの一個前まで)
        step_count = 1
        while len(object_name.Passed_list) > 1:
            #step_n.txtのデータをfieldに格納する
            field = list()
            step_name = 'step_' + str(step_count) + '.txt'
            field = map_func.load_map(step_name,field)
            #次の位置を取り出す
            x,y = object_name.Passed_list[1]
            #次に進む位置が0ならそのまま進む
            #1なら進まない
            if (field[x][y] == 0):
                field[x][y] = 1                
                object_name.Passed_list.pop(0)
            else :
                x,y = object_name.Passed_list[0]
                field[x][y] = 1
                #表示するマップの変更の処理を行う
                object_name.Route_Field[x][y] += 1
            #更新したマップを書き込む
            file_name = 'step_' + str(step_count) + '.txt'
            map_func.write_map(file_name,field)
            step_count += 1
        
        #ゴールにたどり着いたときの処理
        #step_n.txtのデータをfieldに格納する
        field = list()
        step_name = 'step_' +str(step_count) + '.txt'
        field = map_func.load_map(step_name,field)
        #ゴール位置を取り出す
        x,y = object_name.Passed_list[0]
        #フィールドのゴール位置を1で埋める
        field[x][y] = 1
        #更新したマップを書き込む
        file_name = 'step_' + str(step_count) + '.txt'
        map_func.write_map(file_name,field)