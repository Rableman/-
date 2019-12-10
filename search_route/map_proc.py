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