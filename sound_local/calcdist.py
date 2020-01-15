import numpy as np
import math
import rec_sound

def readfunc(filename):
  f = open(filename, "r")
  data = f.readlines()
  func1 = data[0].split(",")
  func2 = data[1].split(",")
  func1[0] = int(func1[0])
  func2[0] = int(func2[0]) 
  for i in range(1,3):
    func1[i] = float(func1[i])
    func2[i] = float(func2[i])
  f.close()
  return func1, func2

class Calcdist: 

    def __init__(self):

        self.rec = rec_sound.Record()
        A, B = readfunc("func.txt")
        #音源周波数        
        #第１音源
        self.freqA = A[0]
        self.sourceA = [0, 5]
        self.funcA = [A[1],A[2]]
        #第２音源
        self.freqB = B[0]
        self.sourceB = [5, 5]
        self.funcB = [B[1],B[2]]
        #位置座標情報
        #     
    def get_dist(self):
        sec = 2 #録音時間
        dist=[0,0]
        source=["A","B"]
        dist[0]= self.calc_dist(self.rec.record(self.freqA,sec), self.freqA)
        dist[1] = self.calc_dist(self.rec.record(self.freqB,sec), self.freqB)

        return dist

    #音の振幅を元に距離を計算 
    def calc_dist(self, amp, freq):

        if freq == self.freqA:
            ret = self.funcA[0] * math.log(amp) + self.funcA[1]
        elif freq == self.freqB:
            ret = self.funcB[0] * math.log(amp) + self.funcB[1]
        return ret

    #座標提供
    def get_coord(self):
        dist = self.get_dist()        
        x, y = self.calc_coord(dist[0], self.cos_rule((dist[0]/10), (dist[1]/10), self.sourceB[0] - self.sourceA[0]))
        return x, y

    #座標算出
    def calc_coord(self, dist, ang):
        u = dist * math.cos(ang)
        v = dist * math.sin(ang)
        x = self.sourceA[0] + round(u)
        y = self.sourceA[1] - round(v)
        return x, y

    #余弦定理
    def cos_rule(self, a, b, c):
        ret = (a**2 + c**2 - b**2)/(2 * a * c)
        ret = math.acos(ret)
        return ret