import numpy as np
from bin_search_list import BinSearchKVPair


tone_to_frequency = {
    'C0':16.35   , 'C#0':17.32   , 'D0':18.35   , 'D#0':19.45   , 'E0':20.60   , 'F0':21.83   , 'F#0':23.12   , 'G0':24.50   , 'G#0':25.96   , 'A0':27.50 , 'A#0':29.14   , 'H0':30.87,
    'C1':32.7    , 'C#1':34.65   , 'D1':36.71   , 'D#1':38.89   , 'E1':41.20   , 'F1':43.65   , 'F#1':46.25   , 'G1':49      , 'G#1':51.91   , 'A1':55    , 'A#1':58.27   , 'H1':61.74,
    'C2':65.41   , 'C#2':69.30   , 'D2':73.42   , 'D#2':77.78   , 'E2':82.41   , 'F2':87.31   , 'F#2':92.50   , 'G2':98      , 'G#2':103.83  , 'A2':110   , 'A#2':116.54  , 'H2':123.47,
    'C3':130.81  , 'C#3':138.59  , 'D3':146.83  , 'D#3':155.56  , 'E3':164.81  , 'F3':174.61  , 'F#3':185     , 'G3':196     , 'G#3':207.65  , 'A3':220   , 'A#3':233.08  , 'H3':246.94,
    'C4':261.63  , 'C#4':277.18  , 'D4':293.66  , 'D#4':311.13  , 'E4':329.63  , 'F4':349.23  , 'F#4':369.99  , 'G4':392     , 'G#4':415.30  , 'A4':440   , 'A#4':466.16  , 'H4':493.88,
    'C5':523.25  , 'C#5':554.37  , 'D5':587.33  , 'D#5':622.25  , 'E5':659.25  , 'F5':698.46  , 'F#5':739.99  , 'G5':783.99  , 'G#5':830.61  , 'A5':880   , 'A#5':932.33  , 'H5':987.77,
    'C6':1046.50 , 'C#6':1108.73 , 'D6':1174.66 , 'D#6':1244.51 , 'E6':1318.51 , 'F6':1396.91 , 'F#6':1479.98 , 'G6':1567.98 , 'G#6':1661.22 , 'A6':1760  , 'A#6':1864.66 , 'H6':1975.53,
    'C7':2093.00 , 'C#7':2217.46 , 'D7':2349.32 , 'D#7':2489.02 , 'E7':2637.02 , 'F7':2793.83 , 'F#7':2959.96 , 'G7':3135.96 , 'G#7':3322.44 , 'A7':3520  , 'A#7':3729.31 , 'H7':3951.07,
    'C8':4186.01 , 'C#8':4434.92 , 'D8':4698.63 , 'D#8':4978.03 , 'E8':5274.04 , 'F8':5587.65 , 'F#8':5919.91 , 'G8':6271.93 , 'G#8':6644.88 , 'A8':7040  , 'A#8':7458.62 , 'H8':7902.13,
}


for i in range(9):
    tone_to_frequency[f'Db{i}'] = tone_to_frequency[f'C#{i}']
    tone_to_frequency[f'Eb{i}'] = tone_to_frequency[f'D#{i}']
    tone_to_frequency[f'Gb{i}'] = tone_to_frequency[f'F#{i}']
    tone_to_frequency[f'Ab{i}'] = tone_to_frequency[f'G#{i}']
    tone_to_frequency[f'Bb{i}'] = tone_to_frequency[f'A#{i}']


frequency_to_tone = {v:k for k,v in tone_to_frequency.items()}


frequency_set = BinSearchKVPair(list(frequency_to_tone.keys()))


def getFrequencies(n_freqs,min_freq,max_freq):
    return list(np.exp(np.linspace(0,np.log(max_freq/min_freq),n_freqs))*min_freq)



class Staves: 
    # a track to be written on a sheet
    # applies voices onto self
    def __init__(self , number_of_staves = 1):
        self.sequential_events = []
        self.timed_effects = []

class Voice:
    def __init__(self):
        self.event_sequence = []



class SequentialEvent:
    def __init__(self , length): 
        self.length = length


class Note(SequentialEvent): pass
class Chord(SequentialEvent): pass
class Rest(SequentialEvent): pass


class Tone:
    def __init__(self , start , duration , tone , amplitude=1 , phase=0):
        self.start = start
        self.duration = duration
        if isinstance(tone,float):
            self.tone = frequency_to_tone[tone]
            self.frequency = tone
        elif isinstance(tone,str):
            self.tone = tone
            self.frequency = tone_to_frequency[tone]
        else:
            raise TypeError(f'type of tone is bad: {type(tone)} - {tone}')        
        self.amplitude = amplitude
        self.phase = phase



class Music:
    def __init__(self , tones):
        self.tones = tones
        first_tone = min(tones , key=lambda tone:tone.start)
        self.global_start = first_tone.start
        last_tone = max(tones , key=lambda tone:tone.start + tone.duration)
        self.global_end = last_tone.start + last_tone.duration
    
    @property
    def duration(self):
        return self.global_end - self.global_start
    
    def toSignal(self , bytes_per_second):
        time_span = self.global_end - self.global_start
        byte_span = int(time_span * bytes_per_second)
        Y = np.zeros(byte_span,dtype=np.float64)
        for tone in self.tones:
            byte_start = int((tone.start - self.global_start) * bytes_per_second)
            byte_end = byte_start + int(tone.duration * bytes_per_second)
            X = np.linspace(0,tone.duration,byte_end-byte_start)
            Y[byte_start:byte_end] += tone.amplitude * np.sin(X * tone.frequency * 2 * np.pi + tone.phase)
        Y /= max(Y.max() , abs(Y.min()))
        return Y