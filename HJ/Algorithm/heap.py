class MaxHeap(object):
    def __init__(self) -> None:
        super().__init__()
        self.queue: List[int] = []
    def swap(self,i,parent_idx): self.queue[i], self.queue[parent_idx] = self.queue[parent_idx], self.queue[i]
    def parent(self,i): return (i-1)//2
    def leftChild(self,i): return i*2+1
    def rightChild(self,i): return i*2+2
    
    def insert(self,n):
        # append to last
        self.queue.append(n)
        last_idx=len(self.queue)-1
        #check child to parent
        while 0<=last_idx:
            parent_idx=self.parent(last_idx)
            if 0<=parent_idx and self.queue[parent_idx]<self.queue[last_idx]:
                self.swap(last_idx,parent_idx)
                last_idx=parent_idx
            else: break
    
    def delete(self):
        last_idx=len(self.queue)-1
        if last_idx<0: return -1
        self.swap(0,last_idx)
        maxv=self.queue.pop()
        self.maxHeapify(0)
        print(maxv)
        return maxv

    def maxHeapify(self,i):
        leftIdx=self.leftChild(i)
        rightIdx=self.rightChild(i)
        maxIdx=i

        if leftIdx<=len(self.queue)-1 and self.queue[maxIdx]<self.queue[leftIdx]:
            maxIdx=leftIdx
        if rightIdx<=len(self.queue)-1 and self.queue[maxIdx]<self.queue[rightIdx]:
            maxIdx=rightIdx

        if maxIdx!=i:
            self.swap(i,maxIdx)
            self.maxHeapify(maxIdx)

if __name__ == '__main__':
    heap=MaxHeap()
    heap.insert(1)
    heap.insert(6)
    heap.insert(3)
    heap.insert(39)
    heap.insert(29)
    heap.insert(229)
    heap.insert(5)
    heap.insert(52)
    heap.insert(521)
    print(heap.queue)
    heap.delete()
    heap.delete()
    heap.delete()
    heap.delete()
    heap.delete()
    heap.delete()yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy