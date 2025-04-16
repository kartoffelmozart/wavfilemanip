from wav_tools import *
from music import tone_to_frequency
from time import time

bef = time()

w = WavFile('sounds/Den blå anemone.wav')
fr = w.fourierRange(0,20)

aft = time()
print('took',aft-bef)
for t in (3,5,7,9,11,13,15,17,19):
    tones = list(fr.prevelantNotesAt(t,10))
    print(tones)
    freqs = [tone_to_frequency[tone] for tone in tones]
    fr.get(t).display()