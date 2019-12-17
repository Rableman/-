#coding utf-8

class map_func:
    def load_map(file_name,var_name):
        #迷路の情報をfieldにリストで格納
        f = open(file_name,'r')
        for row in f:
            row_re = row.replace('\n', '')
            row_new = list()
            for i in row_re: #文字から数値に変換
                row_new.append(int(i))
            var_name.append(list(row_new))
        f.close()
        
    def cal_heuristic(start,goal):
        #ユークリッド距離(平方根は取らない)を計算
        dis = ((goal[0]-start[0])**2+(goal[1]-start[1])**2)**0.5
        return dis

    def cal_distance(path):
        return len(path)
    '''
    def write_map(self,file_name):
        device = random_setup.random_set.rand_map(1,5) #今度ランダムじゃないものに置き換える？
        self.field[device[0]][device[1]] = 1

    def  update_map(self,file_name,object_name,var_name):
        self.field = list()
        object_name.load_map(file_name,var_name)
        for i in range(8):
            object_name.write_map(file_name)
    '''
