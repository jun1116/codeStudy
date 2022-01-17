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

    # k : Key 
    # def insert_node(self,p_pos,p_node,node,key):
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
        # print(key," Node : ",node , pos)
        
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

    # def search_key_with_Parent(self,p_node,node,key):
    #     """ Find Key 
    #     IF FIND : RETURN [Node, Key]
    #     else : RETURN [None, None] """
    #     # print(node)
    #     pos=0
    #     while pos < len(node.keys):
    #         if key[0] == node.keys[pos][0]:
    #             # print(f'Find! key : {node.keys[pos]}')
    #             return p_node, node, key
    #         elif key[0] < node.keys[pos][0] : break
    #         else:
    #             pos+=1
    #     # print(node, pos)
    #     if node.child:
    #         return self.search_key(node, node.child[pos],key)
    #     else : 
    #         return None, None, None
    def search_key(self,node,key):
        """ Find Key 
        IF FIND : RETURN [Node, Key]
        else : RETURN [None, None] """
        # print(node)
        pos=0
        while pos < len(node.keys):
            if key[0] == node.keys[pos][0]:
                # print(f'Find! key : {node.keys[pos]}')
                return node, key
            elif key[0] < node.keys[pos][0] : break
            else:
                pos+=1
        # print(node, pos)
        if node.child:
            return self.search_key(node.child[pos],key)
        else : 
            return None, None
            # return f"NOT FOUND {key}"

    def print_inorder(self,node):
        if node.child:
            for i in range(len(node.keys)):
                self.print_inorder(node.child[i])
                print(node.keys[i])
            self.print_inorder(node.child[-1])
        else:
            for i in node.keys:
                print(i)
            # print(node.keys)
    
    def delete(self,node,key):
        pos = 0
        while pos<len(node.keys) and key[0] > node.keys[pos][0]:
            pos+=1
        if node.isleaf==True and pos<len(node.keys) and node.keys[pos][0]==key[0]:
            node.keys.pop(pos)
            return


        if not node:
            return f"THERE IS NO KEY {key}"
        else:
            if node.isleaf: #Leaf에서 DELETE일경우
                pass
            else: # Internal Node에서 DELETE일경우
                pass
        pass





if __name__=="__main__":
    print("Start")
    bt = BTree(3)
    for i in range(1,50):
        bt.insert_node(bt.root,[i,i*10])
    