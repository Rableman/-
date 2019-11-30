import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt
from scipy import signal
import math

def filt(data, s_freq, fp, fs, gp, gs, ftype):
    nyq = s_freq / 2                           #ナイキスト周波数
    Wp = fp / nyq
    Ws = fs / nyq
    N, Wn = signal.buttord(Wp, Ws, gp, gs)
    b, a = signal.butter(N, Wn, ftype)
    data = signal.filtfilt(b, a, data)
    return data

class PlotFreq:

    def __init__(self):
        #音源周波数
        self.freqA = 15000
        self.sourceA = [0, 50]
        self.freqB = 10000
        self.sourceB = [50, 50]
        self.freqC = 11000
        self.sourceC = [50, 0]

        #マイクインプット設定
        self.CHUNK=1024           #1度に読み取る音声のデータ幅
        self.RATE=44100            #サンプリング周波数
        self.record_seconds=1      #録音時間[ms]
        self.audio=pyaudio.PyAudio()
        self.stream=self.audio.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=self.RATE,
                                    input=True,
                                    frames_per_buffer=self.CHUNK)

        #音声データの格納場所(プロットデータ)
        self.data=np.zeros(self.CHUNK)
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)
        self.db_data = 0

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

    def record(self, freq):
        print("recstart")
        self.data=np.zeros(self.CHUNK)
        for i in range(0, int(self.RATE/self.CHUNK * self.record_seconds)): #秒数を指定して録音
            self.data=np.append(self.data,self.AudioInput())
        self.fft_data=self.FFT_AMP(self.data) #音声データをフーリエ変換
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE) #周波数軸を生成

        #カット処理
        for i in range (len(self.fft_data)):
            if self.axis[i] < freq-100 or self.axis[i] > freq+100:
                self.fft_data[i] = 0
                self.axis[i] = 0
        self.axis = self.axis[self.axis.nonzero()]
        self.fft_data = self.fft_data[self.fft_data.nonzero()]

        #ピーク検出
        maxid = signal.argrelmax(self.fft_data, order=3000)
        self.db_data = max(self.fft_data[maxid])
        print(self.db_data)
        #self.db_data.append(self.fft_data[maxid])

        #debug用
        plt.plot(self.axis, self.fft_data, label="test") 
        plt.plot(self.axis[maxid], self.fft_data[maxid], "ro")
        plt.show()

        #db_val = self.get_db(self.db_data) #デシベル計算
        db_val = self.db_data
        return db_val

    def get_coord(self):
        dist_a = self.calc_dist(self.record(self.freqA))
        dist_b = self.calc_dist(self.record(self.freqB))
        dist_c = self.calc_dist(self.record(self.freqC))
        
        x, y = self.calc_coord(dist_a, self.cos_rule(50, dist_a, dist_b))
        return x, y

    def get_db(self, amp, base = 1.0):
        ret = 20 * math.log10(amp/base)
        print("%2.2f[dB]" % ret)
        return ret
        
    def calc_dist(self, amp):
        #音の減衰式 y = -28.85ln(x) + 83.158
        dist = -28.85 * math.log(amp) + 83.158
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

    def end_rec(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def AudioInput(self):
        ret=self.stream.read(self.CHUNK, exception_on_overflow = False)    #音声の読み取り(バイナリ) CHUNKが大きいとここで時間かかる
        #バイナリ → 数値(int16)に変換
        #32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
        ret=np.frombuffer(ret, dtype="int16")/32768.0
        ret=filt(ret, self.RATE, 16000, 17000, 3, 40, "low")
        return ret

    def FFT_AMP(self, data):
        data=np.hamming(len(data))*data
        data=np.fft.fft(data)
        data=np.abs(data)
        return data

if __name__=="__main__":
    plotwin=PlotFreq()
    x, y = plotwin.get_coord() 
    print("Coordinate: [{0}][{1}]".format(int(x), int(y)))
    plotwin.show_grid()
    plotwin.end_rec()