class BSKVPEntry(list):
    def __init__(self , key , value=None):
        self.append(key)
        if value is not None: self.append(value)
        self.key = key
        self.value = value

    def __hash__(self):
        return hash(self.key)

class BinSearchKVPair(list):
    def __init__(self , keys , values=None , differenceFunc = lambda a,b: abs(a-b) , sorting_key = None):
        values_aux = [None]*len(keys)
        keys_aux = []
        for i,(j,key) in enumerate(sorted(enumerate(keys) , 
                                          key = ( lambda pair: sorting_key(pair[1]) ) 
                                          if sorting_key is not None 
                                          else lambda pair: pair[1])):
            if values: values_aux[i] = values[j] 
            keys_aux.append(key)
        self.extend([BSKVPEntry(key,val) for key,val in zip(keys_aux,values_aux)])
        self.sorting_key = sorting_key
        self.differenceFunc = differenceFunc

    def add(self,key,value=None):
        i = self.binarySearch(key)
        if self[i].key == key:
            self[i] = BSKVPEntry(key , value)
            return
        super().insert(BSKVPEntry(key , value) , i)
    
    def contains(self , key):
        return self.closestKey(key) == key
    
    def keys(self):
        return map(lambda pair: pair.key , self)
    
    def values(self):
        return map(lambda pair: pair.value , self)

    def binarySearch(self , key):
        low,high = 0,len(self)-1
        mid = (low + high) // 2
        while low < high:
            if key < self[mid].key:
                high = mid
                mid = (low + high) // 2
            elif key > self[mid].key:
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
        return self.closestPair(key).key
    
    def get(self , key):
        return self.closestPair(key).value
    
    def floorOf(self , key):
        i = self.binarySearch(key)
        if self[i].key == key:
            return self[i]
        elif i == 0:
            raise IndexError(f'A floor to {key} is not present in {self}')
        else:
            return self[i-1]
    
    def floorKey(self , key):
        return self.floorOf(key).key

    def floorValue(self , key):
        return self.floorOf(key).value
    
    def ceilOf(self , key):
        i = self.binarySearch(key)
        if self[i].key == key:
            return self[i]
        elif i == len(self) - 1:
            raise IndexError(f'A ceiling to {key} is not present in {self}')
        else:
            return self[i+1]

    def ceilKey(self , key):
        return self.ceilOf(key).key
    
    def ceilValue(self , key):
        return self.ceilOf(key).value



if __name__ == '__main__':
    tm = BinSearchKVPair(list(range(10)))
    