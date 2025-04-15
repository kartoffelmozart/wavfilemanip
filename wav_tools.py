import numpy as np
from file_tools import *
from pathlib import Path
from matplotlib import pyplot as plt
from interpret_wav import FourierOnRange
from music import *



class WavFile(FileMethods):
    short_path = 'c:/Windows/WinSxS/amd64_microsoft-windows-speech-userexperience_31bf3856ad364e35_10.0.26100.3037_none_b7f9742dfbb0e755/Speech Sleep.wav'
    short_path = 'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm01.wav'
    many = [
        'c:/Windows/WinSxS/amd64_microsoft-windows-speech-userexperience_31bf3856ad364e35_10.0.26100.3037_none_b7f9742dfbb0e755/Speech Sleep.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm01.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm02.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm03.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm04.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm05.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm06.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm07.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm08.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm09.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/Alarm10.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/chimes.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/chord.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/ding.wav',
        'c:/Windows/WinSxS/amd64_microsoft-windows-shell-sounds_31bf3856ad364e35_10.0.26100.1_none_140624931e1631ac/notify.wav',
    ]
    
    short_empty = 'empty.wav'
    def __init__(self , wav):
        self.path = None
        if isinstance(wav,str) or isinstance(wav,Path):
            with open(wav,'rb') as file:
                self.path = str(wav)
                self.data = np.array(list(file.read()))
        elif isinstance(wav,np.ndarray):
            self.data = wav
        self.sound_data = self.data[40:]
        self.ft = None
    
    def fourCC(self):
        return self.charactersAt(0,4)
    
    def size(self):
        return self.intAt(4)
    
    def samplerate(self):
        return self.intAt(24)
    
    def WAVEChunkIndices(self):
        I = []
        for i in range(0,self.size()+8,4):
            if 'WAVE' == self.charactersAt(i,4):
                I.append(i)
        return I

    def saveAt(self , path = './'):
        with open(path , 'wb') as file:
            file.write(bytes(list(self.data)))

    def duration(self):
        return self.sound_data.shape[0] / self.samplerate() / 4

    def writeSin(self , freq , start=None,end=None):
        if start is None: start = 0
        if end is None: end = len(self.sound_data)
        duration_in_seconds = (end-start) / self.sampleRate() / 4

        X = np.linspace(0,duration_in_seconds,(end-start)//4)
        sin  = np.sin(X*freq*2*np.pi)*20
        tone8 = (sin).astype(np.uint8) + 2**7-1
        tone16 = ((sin).astype(np.uint16) + 2**15-1) % 256
        self.sound_data[start:end:4] = tone8
        self.sound_data[start+1:end:4] = tone16
        self.sound_data[start+2:end:4] = tone8
        self.sound_data[start+3:end:4] = tone16

    def writeSins(self,*sin_infos,start=None,end=None,left=True,right=True,amplitude=(2**7-1)):
        if start is None:
            start = 0
            start_byte = 0
        else:
            start_byte = self.timeToByte(start)
        
        if end is None:
            end = self.duration()
            end_byte = len(self.sound_data)
        else:
            end_byte = self.timeToByte(end)

        duration = end - start
        span = end_byte - start_byte
        X = np.linspace(0,duration,span // 4)
        Y = np.zeros(span // 4,np.float64)
        for info in sin_infos:
            wave = info['amplitude'] * np.sin(X * info['frequency'] * np.pi * 2 + info['phase'])
            Y += wave
        sound_data = (Y / max(Y.max(),abs(Y.min())) * amplitude).astype(np.uint16)
        data8 = sound_data // 256
        data16 = sound_data % 256
        if left:
            self.sound_data[start_byte:end_byte:4] = data8
            self.sound_data[start_byte+1:end_byte:4] = data16
        if right:
            self.sound_data[start_byte+2:end_byte:4] = data8
            self.sound_data[start_byte+3:end_byte:4] = data16

    def writeMusic(self , music , start=0 , left=True , right=True , amplitude=(2**7-1)):
        Y8,Y16 = self.signalToBytes(music.toSignal(self.samplerate())*(amplitude))
        start_byte = self.timeToByte(start)
        end_byte = start_byte + Y8.shape[0]*4
        if left:
            self.sound_data[start_byte:end_byte:4] = Y8
            self.sound_data[start_byte+1:end_byte+1:4] = Y16
        if right:
            self.sound_data[start_byte+2:end_byte:4] = Y8
            self.sound_data[start_byte+3:end_byte+3:4] = Y16

    def signalToBytes(self , signal):
        Y = signal.astype(np.uint16)
        return Y//256 , Y%256
    
    def spanToSignals(self , start_time , end_time , mono=False):
        start_byte,end_byte = self.timeToByte(start_time),self.timeToByte(end_time)
        start_byte -= start_byte%4 ; end_byte -= end_byte%4
        chunk = self.sound_data[start_byte:end_byte].astype(np.int16)
        left8,left16,right8,right16 = (chunk[i::4] for i in (0,1,2,3))
        left_signal,right_signal = ((left8 << 8) + left16) , ((right8 << 8) + right16)
        return left_signal + right_signal if mono else (left_signal,right_signal)
    
    def timeToByte(self , t):
        return int(t * self.samplerate() * 4)
    
    def byteToTime(self , b):
        return b / self.samplerate() / 4
    
    def fourierRange(self , 
                     start_time = 0 , 
                     end_time = None , 
                     sample_duration = .05 , 
                     frequency_range = (16.5,8000) , 
                     n_frequencies=10000):
        
        if end_time is None: end_time = self.duration() - start_time
        signal = self.spanToSignals(start_time,end_time,True)
        return FourierOnRange(
            signal,
            start_time , end_time,
            sample_duration,
            frequency_range=frequency_range,
            n_frequencies=n_frequencies)
   
    @classmethod
    def empty(cls , duration , samplerate=44100):
        total_size = int(duration * samplerate * 4 + 40)
        written_size = total_size - 8
        data = np.zeros(total_size,np.uint8)
        data[:4] = charsToBytes('RIFF')
        data[4:8] = intToBytes(written_size)
        data[8:12] = charsToBytes('WAVE')
        data[12:16] = [102,109,116,32] # fmt
        data[16:24] = [16,0,0,0,1,0,2,0]
        data[24:28] = intToBytes(samplerate)
        data[28:32] = intToBytes(samplerate*4)
        data[32:36] = [4,0,16,0]
        data[36:40] = charsToBytes('data')
        return WavFile(data)



if __name__ == '__main__':
    from make_some_music import mozart
    m = mozart()
    w = WavFile.empty(m.duration)
    fr = w.fourierRange()