import pyaudio
import sys
import time
import wave

chunk = 512 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = chunk
)

all = []
for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
    data = stream.read(chunk)
    all.append(data)

stream.close()
p.terminate()

data = b''.join(all)

import numpy as np
import matplotlib.pyplot as plt

x = np.frombuffer(data, dtype="int16") / 32768.0

plt.figure(figsize=(15,3))
plt.plot(x)
plt.show()

x = np.fft.fft(np.frombuffer(data, dtype="int16"))

plt.figure(figsize=(15,3))
plt.plot(x.real[:int(len(x)/2)])
plt.show()