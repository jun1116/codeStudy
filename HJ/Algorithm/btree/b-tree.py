class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf=leaf
        self.keys=[]
        self.child=[]
class Bree:
    def __init__(self, t):
        self.root=BTreeNode(True)
        # 't' is order of B Tree
        self.t=t
    
    def print_tree(self,x,l=0):
        print("Lebel " ,1 , " ", len(x.keys), end=":")
        for i in x.keys:
            print(i,end=" ")
        print()
        l+=1
        if len(x.child)>0:
            for i in x.child: self.print_tree(i,1)
    def search(self, k, x=None):
        ''' Search for key "k" at position 'x'.
        If 'x' is not specified, then search occurs from root.
        Return 'None' if 'k' is not found.
        Otherwise returns a tuple of node and index at which the key was found.
        Auguments: 
          k -- key to be searched
          x -- position to search from
        '''
        if x != None:
            i=0
            while i<len(x.keys) and k>x.keys[i][0]:
                i+=1
            if i<len(x.keys) and k==x.keys[i][0]:
                return (x,i)
            elif x.leaf:
                return None
            else:
                # Search children
                return self.search(k,x.child[i])
        else:
            # Search entire tree as node not proiveded
            return self.search(k,self.root)
    
    def insert(self,k): 
        """ Calls helper  functions to insert key 'k' in the B-Tree
        k : Key to be inserted"""
        if len(root.keys)==(2*self.t)-1:
            temp=BTreeNode()
            self.root=temp
            # Former root becomed 0th child of new root 'temp'
            temp.child.insert(0,root)
            self._split_child(temp,0)
            self._insert_nonfull(temp,k)
        else:
            self._insert_nonfull(root,k)
    
    def _insert_nonfull(self,x,k):
        """ Insert key 'k' at position 'x' in a non-full node
        x :: Position of Node
        k :: key to be inserted """
        i = len(x.keys)-1
        if x.leaf:
            x.keys.append((None,None))
            while i>=0 and k[0]<k.keys[i][0]:
                x.keys[i+1] = x.keys[i]
                i -= 1
            x.keys[i+1]=k
        else:
            while i>=0 and k[0]<x.keys[i][0]:
                i-=1
            i+=1
            if len(x.child[i].keys)==(2*self.t)-1:
                self._split_child(x,i)
                if k[0] > x.keys[i][0]:
                    i+=1
            self._insert_nonfull(x.child[i],k)
    
    def _split_child(self,x,i):
        """ Split the child of node at 'x' from index 'i' 
        x : parent node of the node to be split
        i : index value of the child """
        t=self.t
        y=x.child[i]
        z=BTreeNode(y.leaf)
        x.child.insert(i+1,z)
        x.keys.insert(i,y.keys[t-1])
        z.keys = y.keys[t:(2*t)-1]
        y.keys = y.keys[0:t-1]
        if not y.leaf:
            z.child = y.child[t:2*t]
            y.child = y.chilid[0:t-1]
