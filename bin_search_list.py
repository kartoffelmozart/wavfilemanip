class BinSearchKVPair(list):
    def __init__(self , keys , values=None , differenceFunc = lambda a,b: abs(a-b) , sorting_key = None):
        if values:
            values_aux = [None]*len(keys)
            keys_aux = []
            for i,(j,key) in enumerate(sorted(enumerate(keys) , key=( lambda pair: sorting_key(pair[1]) ) if sorting_key is not None else lambda pair: pair[1])):
                values_aux[i] = values[j] if values else None
                keys_aux.append(key)
            self.extend([(key,val) for key,val in zip(keys_aux,values_aux)])
        else:
            self.extend([(key,) for key in sorted(keys)])
        self.sorting_key = sorting_key
        self.differenceFunc = differenceFunc

    def add(self,key,value=None):
        super().insert((key,value) if value else (key,) , self.binarySearch(key))
    
    def contains(self , key):
        i = self.binarySearch(key)
        return self[i][0] == key
    
    def keys(self):
        return map(lambda pair: pair[0] , self)
    
    def values(self):
        return map(lambda pair: pair[1] , self)

    def binarySearch(self , key):
        low,high = 0,len(self)-1
        mid = (low + high) // 2
        while low < high:
            if key < self[mid][0]:
                high = mid
                mid = (low + high) // 2
            elif key > self[mid][0]:
                low = mid+1
                mid = (low + high) // 2
            else:
                return mid
        mn = (float('inf'),)
        for i in range(max(0,mid-1),min(mid+2,len(self))):
            diff = self.differenceFunc(key,self[i][0])
            if diff < mn[0]:
                mn = (diff , i)
        return mn[1]
    
    def closestPair(self , key):
        return self[self.binarySearch(key)]
    
    def closestKey(self , key):
        return self.closestPair(key)[0]
    
    def get(self , key):
        return self.closestPair(key)[1]



if __name__ == '__main__':
    tm = BinSearchKVPair(list(range(10)))
    