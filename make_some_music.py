
from music import Music,Tone

def mozart():
    tones = [
        Tone(0,.25,'H5'),
        Tone(.25,.25,'A5'),
        Tone(.5,.25,'G#5'),
        Tone(.75,.25,'A5'),           
        Tone(1,.5,'C6'),            Tone(1,.5,'A3'),
                                    Tone(1.5,.25,'C4'),Tone(1.5,.25,'E4'),
        Tone(2,.25,'D6'),           Tone(2,.25,'C4'),Tone(2,.25,'E4'),
        Tone(2.25,.25,'C6'),
        Tone(2.5,.25,'H5'),         Tone(2.5,.25,'C4'),Tone(2.5,.25,'E4'),
        Tone(2.75,.25,'C6'),        
        Tone(3,.5,'E6'),            Tone(3,.5,'A3'),
                                    Tone(3.5,.25,'C4'),Tone(3.5,.25,'E4'),
        Tone(4,.25,'F6'),           Tone(4,.25,'C4'),Tone(4,.25,'E4'),
        Tone(4.25,.25,'E6'),
        Tone(4.5,.25,'D#6'),        Tone(4.5,.25,'C4'),Tone(4.5,.25,'E4'),
        Tone(4.75,.25,'E6'),
        Tone(5,.25,'H6'),           Tone(5,.5,'A3'),
        Tone(5.25,.25,'A6'),
        Tone(5.5,.25,'G#6'),        Tone(5.5,.25,'C4'),Tone(5.5,.25,'E4'),
        Tone(5.75,.25,'A6'),
        Tone(6,.25,'H6'),           Tone(6,.5,'A3'),
        Tone(6.25,.25,'A6'),
        Tone(6.5,.25,'G#6'),        Tone(6.5,.25,'C4'),Tone(6.5,.25,'E4'),
        Tone(6.75,.25,'A6'),
        Tone(7,1,'C7'),             Tone(7,1,'A3'),Tone(7,1,'C4'),Tone(7,1,'E4'),
    ]    
    m = Music(tones)
    return m


def see():
    t = 60
    w = WavFile.empty(t)
    m = Music([Tone(0,60,t) for t in ('A3','E3','H4','C#5','G#5')])
    w.writeMusic(m)
    # w.saveAt('sounds/amaj960.wav')
    X = np.linspace(0,127,t*44100)
    w.writeMusic(m,amplitude=X)
    w.saveAt('sounds/music0-127.wav')
    w.writeSins(*[{'frequency':tone_to_frequency[t],'phase':0,'amplitude':1} for t in ('A3','E3','H4','C#5','G#5')],amplitude=X)
    w.saveAt('sounds/sines0-127.wav')


def Am9(duration=1):
    return Music([Tone(0,duration,t) for t in ('A3','E4','H4','C5','G5')])


    #for mag in range()
if __name__ == '__main__':
    from wav_tools import WavFile,np,tone_to_frequency

    # mozart()
    t = 60
    w = WavFile.empty(t)
    m = Music([Tone(0,t,tone) for tone in ('A3','E3','H4','C#5','G#5')])
    w.writeMusic(m)
    w.display(np.int8)