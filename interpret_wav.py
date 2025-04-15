from make_some_music import mozart
from matplotlib import pyplot as plt
from bin_search_list import BinSearchKVPair
from music import getFrequencies,Music,Tone,frequency_set,frequency_to_tone
import numpy as np


def rainbow(n):
    r,g,b = 255,0,0
    dr,dg,db = -255 // n , 255 // n // 2 , 255 // n
    for i in range(n):
        yield (r,g,b)
        r += dr ; g += dg ; b += db
        if i == n // 2: dg = -dg
    yield from rainbow(n)


class LinspaceFactory:
    cache = {}

    @classmethod
    def getLinspace(cls , start , end , n):
        key = (start,end,n)
        if key not in cls.cache:
            cls.cache[key] = np.linspace(*key)
        return cls.cache[key]

class FourierTransformation:
    Ts = {}
    def __init__(self , freq_to_prevelancy):
        self.ftp = freq_to_prevelancy
        self.min_freq,self.max_freq = self.ftp[0][0] , self.ftp[-1][0]
        self.local_maxima = None

    def display(self , marks=[]):
        plt.plot(*zip(*self.ftp))
        plt.scatter(marks,[1]*len(marks))
        plt.show()

    def prevelanceOf(self , freq):
        if freq > self.max_freq or freq < self.min_freq:
            raise ValueError(f'Frequency is out of bounds. The sample was only analysed in the range {self.min_freq} - {self.max_freq}')
        freq,val = self.ftp.closestPair(freq)
        return val,freq
    
    def mostPrevelant(self , n):
        if self.local_maxima is None: 
            self.findLocalMaxima()
        return map(
            lambda pair:frequency_to_tone.get(
                frequency_set.closestKey(pair[1])) , 
                self.local_maxima[-n:]
            )

    def findLocalMaxima(self): # fpm means frequency_prevalence_map
        local_maxima = set()
        if self.ftp[0][1] > self.ftp[1][1]:
            local_maxima.add(self.ftp[0])
        if self.ftp[1][1] > self.ftp[0][1] and \
        self.ftp[1][1] > self.ftp[2][1]:
            local_maxima.add(self.ftp[1])
        if self.ftp[-1][1] > self.ftp[-2][1]:
            local_maxima.add(self.ftp[-1])
        if self.ftp[-2][1] > self.ftp[-1][1] and \
       self.ftp[-2][1] > self.ftp[-3][1]:
            local_maxima.add(self.ftp[-2])
        for i in range(2,len(self.ftp)-2):
            pair1,pair2,pair3,pair4,pair5 = self.ftp[i-2:i+3]
            if pair3[1] > pair2[1] and pair3[1] > pair4[1]:
                local_maxima.add(pair3)
            elif pair3[1] == pair2[1]:
                if pair2[1] > pair1[1]:
                    local_maxima.add(pair2)
            elif pair3[1] == pair4[1]:
                if pair4[1] > pair5[1]:
                    local_maxima.add(pair3)
        prevelencies,frequencies = [],[]
        for pair in local_maxima:
            prevelencies.append(pair[1])
            frequencies.append(pair[0])
        self.local_maxima = BinSearchKVPair(prevelencies,frequencies)

    @classmethod
    def of(cls , signal , frequencies , sample_duration):
        T = LinspaceFactory.getLinspace(0,sample_duration,signal.shape[0]) # T is the time-axis
        prevelancies = []
        for freq in frequencies:
            prevelancies.append(cls.findPrevelanceOfFrequency(signal,freq,T))
        return cls(BinSearchKVPair(frequencies,prevelancies))
    
    @classmethod
    def findPrevelanceOfFrequency(cls,signal,freq,T):
        return np.abs((signal * np.exp(2 * np.pi * 1j * freq * T)).sum())


class FourierOnRange(BinSearchKVPair):
    def __init__(
            self, 
            signal, 
            start_time, 
            end_time, 
            sample_duration, 
            frequency_range=(16.5,8000),
            n_frequencies=10000
                ):
        
        sample_length = int(signal.shape[0] / (end_time - start_time) * sample_duration)
        frequencies = getFrequencies(n_frequencies , *frequency_range)
        fts = []
        times = []
        for i in range(0 , signal.shape[0] , sample_length):
            sample = signal[i:i+sample_length]
            ft = FourierTransformation.of(sample,frequencies,sample_duration)
            times.append(sample_duration * i)
            fts.append(ft)
        super().__init__(times,fts)

    def prevelantNotesAt(self , t , n_notes):
        return self.closestPair(t)[1].mostPrevelant(n_notes)
    
    def showTransformationAt(self , t , marks=[]):
        tf = self.closestPair(t)[1]
        tf.display(marks)

    




if __name__ == '__main__': 
    freqs = list(range(10))
    prevs = [0,1,2,0,3,2,0,1,2,1]
    freq2prev = BinSearchKVPair(freqs,prevs)
    ft = FourierTransformation(freq2prev)
    ft.mostPrevelant(3)
