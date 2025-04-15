from wav_tools import *
from make_some_music import mozart,Am9

m = Am9(3)
w = WavFile.empty(m.duration)
w.writeMusic(m)
w.saveAt('sounds/Am9.wav')
w.display(astype=np.int8)
fr = w.fourierRange(0,.1,frequency_range=(50,1500),n_frequencies=1000)

top5 = list(fr.prevelantNotesAt(0,5))
print(*top5,sep='\n')

fr.showTransformationAt(0,[tone_to_frequency[tone] for tone in top5])

