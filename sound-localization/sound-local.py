import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt
from scipy import signal

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
        self.freqB = 12000
        self.freqC = 11000

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
        self.frq_data = []
        self.db_data = []

        #位置座標情報
        self.grid = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]

    def record(self):
        print("recstart")
        self.data=np.zeros(self.CHUNK)
        for i in range(0, int(self.RATE/self.CHUNK * self.record_seconds)): #秒数を指定して録音
            self.data=np.append(self.data,self.AudioInput())
        self.fft_data=self.FFT_AMP(self.data) #音声データをフーリエ変換
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE) #周波数軸を生成

        #カット処理用
        for i in range (len(self.fft_data)):
            if self.axis[i] < 10000 or self.axis[i] > 16000:
                self.fft_data[i] = 0
                self.axis[i] = 0
        self.axis = self.axis[self.axis.nonzero()]
        self.fft_data = self.fft_data[self.fft_data.nonzero()]
        #debug用
        #plt.plot(self.axis, self.fft_data, label="test") 
        #plt.plot(self.axis[maxid], self.fft_data[maxid], "ro")
        #plt.show()

    def get_coord(self):
        #ピーク検出
        maxid = signal.argrelmax(self.fft_data, order=1000)
        self.db_data.append(self.fft_data[maxid])
        

        
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
    for i in range(0,1):
        plotwin.record()
    print(plotwin.db_data)

    plotwin.end_rec()