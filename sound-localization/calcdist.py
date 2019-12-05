import numpy as np
import math
import rec_sound as rec

class Calcdist: 

    def __init__(self):
        #音源周波数
        self.freqA = 18400
        self.sourceA = [0, 50]
        self.freqB = 18700
        self.sourceB = [50, 50]
        self.freqC = 15000
        self.sourceC = [50, 0]

        #位置座標情報
        self.grid = self.init_grid()

    def init_grid(self):
        grid_num = 5
        grid = [[0 for i in range(grid_num)] for i in range(grid_num)]
        return grid

    def set_grid(self, coord_x, coord_y):
        self.init_grid()
        self.grid[coord_x][coord_y] = 1

    def show_grid(self):
        self.set_grid(0,0)
        for x in range(5):
            print(self.grid[x])

    
    def get_coord(self):
        dist_a = self.calc_dist(rec.Record.record(self.freqA), self.freqA)
        dist_b = self.calc_dist(rec.Record.record(self.freqB), self.freqB)
        
        x, y = self.calc_coord(dist_a, self.cos_rule(50, dist_a, dist_b))
        return x, y

    def calc_dist(self, amp, freq):
        #11000Hz: y = -28.85ln(x) + 83.158
        #21000Hz: y = -32.8ln(x) + 60.863
        if freq == self.freqA:
            dist = -28.85 * math.log(amp) + 83.158
        elif freq == self.freqB:
            dist = -32.81 * math.log(amp) + 60.863
        elif freq == self.freqC:
            dist = 0
        print("%2.2lf[cm]" % dist)
        return dist

    def cos_rule(self, a, b, c):
        ret = (a**2 + c**2 - b**2)/(2 * a * c)
        ret = math.acos(ret)
        return ret

    def calc_coord(self, dist, ang):
        u = dist * math.cos(ang)
        v = dist * math.sin(ang)
        theta = math.atan((self.sourceA[1]-self.sourceB[1])/(self.sourceA[0]-self.sourceB[0]))
        rotsin, rotcos = math.sin(theta), math.cos(theta)
        rot = np.matrix([[rotcos, -rotsin],[rotsin, rotcos]])
        coord = rot * np.matrix([[u],[v]]) + np.matrix([[self.sourceA[0]],[self.sourceA[1]]])
        x = coord[0]
        y = coord[1]
        return x, y