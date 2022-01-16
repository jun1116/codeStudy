# Node
class Node:
    def __init__(self, isleaf=False):
        self.isleaf=isleaf
        self.keys=[]
        self.child=[]
    def __repr__(self):
        return f'k:{self.keys}'
    def split(self):
        length = len(self.keys)
        temp = Node(self.isleaf)
        mid = self.keys[length//2]
        temp.keys = self.keys[length//2+1:]
        self.keys = self.keys[:length//2]
        if self.child:
            temp.child = self.child[length//2+1:]
            self.child = self.child[:length//2+1]
        return self,mid,temp
        

class BTree:
    def __init__(self, m):
        self.m=m #차수 -> m개의 child를 가질 수 있음
        self.root=Node(True)
        # self.root.isleaf = 'root'
        # self.root=None

    def printTree(self, node ,level=0):
        print(f'level {level} , length : {len(node.keys)} ', end=" : ")
        for i in node.keys: 
            print(i[0],end=" ")
        level+=1
        if len(node.child)>0:
            for i in node.child: 
                self.printTree(i, level)
        
    # def splitNode(self,p_pos,p_node,node):
    #     pass

    
    # def insert(self,key):
        # if self.root



    def insert_node(self,node,key):
        """ 데이터 추가하는것, Root부터 시작해서 내려가도록 Trigger가 발동되며, 
        현재의 노드(node)가 leaf가 아닐경우, 재귀적으로 child를 내려감. 
        리프에서의 삽입이 이뤄지고나면, 그대로 자기자신만 반환하고, 
        Leaf에서의 삽입이 OverFlow가 일어날경우 중간key와 자기자신을 반환
        삽입을 하고난 이후, 반환되는 key가 있다면, 해당 child에서 OverFlow가 난것이므로, 관련연산 진행
        """
        pos=0
        while pos < len(node.keys):
            # print(pos)
            if key[0]==node.keys[pos][0]:
                #Duplicate
                print(f"Duplicates key {key}")
                return node, None 
            elif key[0]<node.keys[pos][0]: break
            pos+=1
        print(key," Node : ",node , pos)
        
        # Position 찾기 완료
        if node.isleaf==True : # Leaf라면?? -> Leaf에서의 삽입 로직
            i=len(node.keys)-1
            node.keys.append([1e9,None])
            while i>=0 and key[0]<node.keys[i][0]:
                node.keys[i+1]=node.keys[i]
                i-=1
            node.keys[i+1]=key
            if len(node.keys) >= self.m : # 오버플로 발생?
                if node == self.root:
                    # print("Root OverFlow")
                    ll,mid,rr=node.split()
                    self.root=Node(False)
                    self.root.keys.append(mid)
                    self.root.child.append(ll)
                    self.root.child.append(rr)
                    return self.root, None
                else:
                    # print("Leaf OVERFLOW",node)
                    return node, node.keys[(self.m//2)]

            else: return node, None
        # elif node.isleaf == False: #Leaf가 아니라면?
        else: #Leaf가 아니라면?
            node.child[pos], child_mid_kv = self.insert_node(node.child[pos],key)
            if child_mid_kv: # Child에서 OverFlow발생 -> 자기에 추가시켜줘야해
                ll,mid,rr=node.child[pos].split()

                i=len(node.keys)-1
                node.keys.append([1e9,None])
                node.child.append([])
                while i>=0 and mid[0] < node.keys[i][0]:
                    node.keys[i+1]=node.keys[i]
                    node.child[i+2]=node.child[i+1]
                    i-=1
                node.keys[i+1]=mid
                # i=len(node.child)-1
                node.child[i+2]=rr
                if len(node.keys) >= self.m : # 오버플로 발생?
                    if node == self.root:
                        # print("Root OverFlow")
                        ll,mid,rr=node.split()
                        self.root=Node(False)
                        self.root.keys.append(mid)
                        self.root.child.append(ll)
                        self.root.child.append(rr)
                        return self.root, None
                if len(node.keys)>=self.m:
                    return node, node.keys[(self.m//2)]
            return node, None
            



if __name__=="__main__":
    print("Start")
    bt = BTree(3)
    bt.insert_node(bt.root,[10,11])
    bt.insert_node(bt.root,[30,11])
    bt.insert_node(bt.root,[20,11])  
    bt.insert_node(bt.root,[40,11])
    bt.insert_node(bt.root,[50,11])
    bt.insert_node(bt.root,[60,11])
    bt.insert_node(bt.root,[70,11])
    bt.insert_node(bt.root,[80,11])
    bt.insert_node(bt.root,[90,11])
