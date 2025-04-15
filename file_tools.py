import numpy as np
import cv2
import keyboard as kb
from time import time,sleep

class FileMethods:
    def display(self,astype=np.uint8):
        if astype == np.int8:
            displayBytes(self.data.astype(np.int8) + 127)
        else:
            displayBytes(self.data.astype(astype))

    def chunkAt(self , i , length=4):
        return self.data[i:i+length]

    def intAt(self,i):
        return bytesToInt(self.data[i:i+4])
    
    def charactersAt(self , i , length=4):
        return bytesToChars(self.data[i:i+length])
    
class ByteDisplay:
    def __init__(self , file , astype=np.uint8):
        self.cd = ClickDetect(esc=self.quit , left=self.left , right=self.right)
        self.display_range = (0,1024)
        self.screen_buffer = np.zeros((256,1024,3) , np.uint8)
        self.data = self.getData(file)
        if astype == np.int8:
            self.data = self.data.astype(np.int8) + 127
        else:
            self.data = self.data.astype(astype)
        self.last = self.data.shape[0] - self.data.shape[0] % 1024 + 1024
        self.prev_chunk = self.data[:1024]
        self.markers = []

    def quit(self):
        self.cd.running = False
        cv2.destroyAllWindows()

    def left(self):
        start = max(0,self.display_range[0] - 1024)
        end = start + 1024
        self.display_range = (start,end)
        self.show()

    def right(self):
        end = min(self.display_range[1] + 1024 , self.last)
        start = end - 1024
        self.display_range = (start,end)
        self.show()

    def show(self):
        start,end = self.display_range
        chunk = self.data[start:end]
        end = min(end , start + chunk.shape[0])

        self.screen_buffer[:] = 0
        self.drawMarkers()
        self.screen_buffer[chunk , list(range(end-start))] = 255
        cv2.imshow('bytes',self.screen_buffer)
        cv2.waitKey(1)
        cv2.waitKey(1)
        print(f'bytes {start} - {end}')

    def addMarker(self , i , colour):
        self.markers.append((i,colour))

    def removeMarker(self , i , colour):
        self.markers.remove((i,colour))
    
    def clearMarkers(self):
        self.markers = []
        
    def loop(self):
        self.show()
        self.cd.loop()

    def getData(self , file):
        if isinstance(file,np.ndarray):
            return file
        elif isinstance(file,str):
            with open(file,'rb') as f:
                data = f.read()
            return np.array(list(data))
        elif isinstance(file,bytes):
            return np.array(list(data))
        elif isinstance(file,list):
            return np.array(file)
        
    def drawMarkers(self):
        start,end = self.display_range
        for i,colour in self.markers:
            if start <= i < end:
                self.screen_buffer[:,i-start] = colour


def displayBytes(file , astype=np.uint8):
    ByteDisplay(file , astype).loop()


class ClickDetect:
    def __init__(self , **key_to_callback):
        self.keys = {key:0 for key in key_to_callback}
        self.key_to_callback = key_to_callback

    def loop(self):
        self.running = True
        self.start = time()
        while self.running:
            self.takeInput()
            self.reactToInput()
            self.capFrames(30)

    def takeInput(self):
        for key in self.keys:
            if kb.is_pressed(key):
                self.keys[key] += 1
            else:
                self.keys[key] = 0
    
    def reactToInput(self):
        for key,k in self.keys.items():
            if k == 1:
                self.key_to_callback[key]()

    def capFrames(self , fps):
        diff = time() - self.start
        too_little = 1 / fps - diff
        if too_little > 0:
            sleep(too_little)
        self.start = time()

        
def charsToBytes(chars):
    return list(map(ord,chars))

def bytesToInt(b):
    return int(b[0]) + (int(b[1]) << 8) + (int(b[2]) << 16) + (int(b[3]) << 24)

def intToBytes(i):
    b = []
    for _ in range(4):
        b.append(i%256)
        i //= 256
    return b

def bytesToChars(b):
    return ''.join((map(chr,b)))