import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt

class PlotFreq:
    def __init__(self):
        #マイクインプット設定
        self.CHUNK=256           #1度に読み取る音声のデータ幅
        self.RATE=44100             #サンプリング周波数
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

    def record(self):
        print("recstart")
        self.data=np.zeros(self.CHUNK)
        for i in range(0, int(self.RATE/self.CHUNK * self.record_seconds)):
            self.data=np.append(self.data,self.AudioInput())
        self.fft_data=self.FFT_AMP(self.data)
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)
        for i in range (len(self.fft_data)):
            if self.axis[i] < 10000:
                self.fft_data[i] = 0
                self.axis[i] = 0
        self.axis = self.axis[self.axis.nonzero()]
        self.fft_data = self.fft_data[self.fft_data.nonzero()]
        plt.plot(self.axis, self.fft_data, label="test")
        plt.show()
        self.frq_data.append(self.axis[list(self.fft_data).index((max(self.fft_data)))])
        self.db_data.append(max(self.fft_data))


    def end_rec(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()


    def AudioInput(self):
        ret=self.stream.read(self.CHUNK, exception_on_overflow = False)    #音声の読み取り(バイナリ) CHUNKが大きいとここで時間かかる
        #バイナリ → 数値(int16)に変換
        #32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
        ret=np.frombuffer(ret, dtype="int16")/32768.0
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
    #plt.plot(plotwin.db_data, label = "db data")
    #plt.show()

    plotwin.end_rec()