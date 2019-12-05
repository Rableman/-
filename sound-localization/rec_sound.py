import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from scipy import signal
import math
import csv

def div_list(lists, num):
    if len(lists) == 1:  return lists[0]
    for i in range(len(lists)):
        lists[i] = lists[i]/num
    return lists   

def filt(data, s_freq, fp, fs, gp, gs, ftype):
    nyq = s_freq / 2                           #ナイキスト周波数
    Wp = div_list(fp,nyq)
    Ws = div_list(fs,nyq)
    N, Wn = signal.buttord(Wp, Ws, gp, gs)
    b, a = signal.butter(N, Wn, ftype)
    data = signal.filtfilt(b, a, data)
    return data

class Record:

    def __init__(self):
        #マイクインプット設定
        self.CHUNK=1024           #1度に読み取る音声のデータ幅
        self.RATE=44100            #サンプリング周波数
        self.audio=pyaudio.PyAudio()
        self.stream=self.audio.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=self.RATE,
                                    input=True,
                                    frames_per_buffer=self.CHUNK)

    #集音
    def AudioInput(self, freq):
        ret=self.stream.read(self.CHUNK, exception_on_overflow = False)    #音声の読み取り(バイナリ) CHUNKが大きいとここで時間かかる
        #バイナリ → 数値(int16)に変換
        #32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
        ret=np.frombuffer(ret, dtype="int16")/32768.0
        #bandpassフィルタ
        ret=filt(ret, self.RATE, [freq-100, freq+100], [freq-200, freq+200], 3, 40, "band")
        return ret

    #フーリエ変換と正規化
    def FFT_AMP(self, data):
        data=np.hamming(len(data))*data
        data=np.fft.fft(data)
        data=np.abs(data)
        return data
    
    #周波数と録音時間を指定
    def record(self, freq, record_seconds):
        #print("recstart", freq)
        self.data=np.zeros(self.CHUNK)

        #録音
        for i in range(0, int(self.RATE/self.CHUNK * record_seconds)): #秒数を指定して録音
            self.data=np.append(self.data,self.AudioInput(freq))

        self.fft_data=self.FFT_AMP(self.data) #音声データをフーリエ変換
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE) #周波数軸を生成

        #カット処理(+-100Hz)
        for i in range (len(self.fft_data)):
            if self.axis[i] < freq-1000 or self.axis[i] > freq+1000:
                self.fft_data[i] = 0
                self.axis[i] = 0
        self.axis = self.axis[self.axis.nonzero()]
        self.fft_data = self.fft_data[self.fft_data.nonzero()]

        #ピーク検出
        maxid = signal.argrelmax(self.fft_data, order=3000)
        db_val = max(self.fft_data[maxid])
        print(db_val)

        #debug用
        plt.plot(self.axis, self.fft_data, label="test") 
        plt.plot(self.axis[maxid], self.fft_data[maxid], "ro")
        plt.show()

        self.get_db(db_val)
        return db_val

    #デシベル計算
    def get_db(self, amp, base = 1.0):
        ret = 20 * math.log10((amp/base))
        print("%2.2f[dB]" % ret)
        return ret

    #録音終了
    def end_rec(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

if __name__=="__main__":
    plotwin=Record()
    freq = int(input("input freq"))
    rec_sec = int(input("input recsec"))
    fd = open("Freqdata.csv", "a+")

    for i in range(1):
        print(plotwin.record(freq, recsec), file=fd)

    fd.close()
    
    plotwin.end_rec()