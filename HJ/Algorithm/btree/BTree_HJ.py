# Node
class Node:
    def __init__(self, isleaf=False):
        self.isleaf=isleaf
        self.keys=[]
        self.child=[]

class BTree:
    def __init__(self, m):
        self.m=m #차수
        self.root=Node(True)

    def printTree(self, node ,level=0):
        print(f'level {level} : {len(node.keys)}', end=" : ")
        for i in node.keys: print(i,end=", ")
        level+=1
        if len(node.child)>0:
            for i in node.child: self.printTree(i, level)
        
    # k : Key 
    def insert(self,k):
        root=self.root
        if len(root.keys)==(2*self.m)-1 : #Maximum number of key
            temp=Node()
            self.root=temp
            temp.child.insert(0,root)
            self.split_child(temp,0)
            self.insert_non_full(temp,k)
        else: # Enough Num of key
            self.insert_non_full(root,k)

    def insert_non_full(self, node, k):
        """ 
        Insert Key k at a not-full node 
        K : [key, value]
        """
        i = len(node.keys)-1
        if node.isleaf: 
            # 리프노드
            node.keys.append((None,None))
            while i>=0 and k[0] < node.keys[i][0]:
                #한칸씩 뒤로 밀기 (i는 끝에서부터 하나씩 작아직)
                node.keys[i+1]=node.keys[i]
                i-=1
            #while문이 끝날땐, k의 값이 node.keys[i][0]보다 큰상태 또는 -1일테니 그 바로 뒤에 삽입
            node.keys[i+1]=k
        else: # Leaf가 아닌노드
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
        temp = Node(node_child.isleaf)
        node.child.insert(i+1, temp)
        node.keys.insert(i,node_child.keys[m-1])
        temp.keys = node_child.keys[m:(2*m)-1]
        node_child.keys = node_child.keys[:m-1]

        if not node_child.isleaf:
            temp.child=node_child.child[m:2*m]
            node_child.child = node_child.child[:m-1]


if __name__=="__main__":
    print("Start")
    bt = BTree(3)
    kvs = [[1,11],[2,22],[5,55],[6,66],[4,44],[3,33]]
    kvs.printTree()
