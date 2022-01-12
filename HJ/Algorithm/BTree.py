# Node
class Node:
    def __init__(self, leaf=False):
        self.leaf=leaf
        self.keys=[]
        self.child=[]

class BTree:
    def __init__(self, m):
        self.root=Node(True)
        self.m=m #차수
    
    # k : Key 
    def insert(self,k):
        root=self.root
        if len(root.keys)==(2*self.m)-1 : #Minimum number of key
            temp=Node()
            self.root=temp
            temp.child.insert(0,root)
            self.split_child(temp,0)
            self.insert_non_full(temp,k)
        else: # Enough Num of key
            self.insert_non_full(root,k)

    def insert_non_full(self,node,k):
        """ 
        Insert Key k at a non-full node 
        """
        i = len(node.keys)-1
        if node.leaf: # It is Leaf Node
            node.keys.append((None,None))
            while i>=0 and k[0] < node.keys[i][0]:
                #한칸씩 뒤로 밀기 (i는 끝에서부터 하나씩 작아직)
                node.keys[i+1]=node.keys[i]
                i-=1
            #while문이 끝날땐, k의 값이 node.keys[i][0]보다 큰상태 또는 -1일테니 그 바로 뒤에 삽입
            node.keys[i+1]=k
        else: # It is Not Leaf
            while i>=0 and k[0]<node.keys[i][0]:
                i-=1
            i+=1
            #위와 동일하게 위치찾기.
            #만약 해당 자식의 키수가 
            if len(node.child[i].keys)==(2*self.m)-1:
                self.split_child(node,i)
                if k[0] > node.keys[i][0]:
                    i+=1
                self.insert_non_full(node.child[i],k)
    
    # Split Child
    def split_child(self, node, i):
        m = self.m
        node_child = node.child[i]
        temp = Node(node_child.leaf)
        node.child.insert(i+1, temp)
        node.keys.insert(i,node_child.keys[m-1])
        temp.keys = node_child.keys[m:(2*m)-1]
        node_child.keys = node_child.keys[:m-1]

        if not node_child.leaf:
            temp.child=node_child.child[m:2*m]
            node_child.child = node_child.child[:m-1]

