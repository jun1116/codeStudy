# Searching a key on a B-tree in Python


# Create a node
class BTreeNode:
  def __init__(self, leaf=False):
    self.leaf = leaf
    self.keys = []
    self.child = []


# Tree
class BTree:
  def __init__(self, t):
    self.root = BTreeNode(True)
    self.t = t

    # Insert node
  def insert(self, k):
    root = self.root
    if len(root.keys) == (2 * self.t) - 1: #최소개수상태라면 -> 쪼개
      temp = BTreeNode()
      self.root = temp
      temp.child.insert(0, root)
      self.split_child(temp, 0)
      self.insert_non_full(temp, k)
    else:
      self.insert_non_full(root, k)

    # Insert nonfull x:new BTreeNode or Root , k : value
  def insert_non_full(self, x, k):
    i = len(x.keys) - 1
    if x.leaf:
      x.keys.append((None, None))
      while i >= 0 and k[0] < x.keys[i][0]:
        x.keys[i + 1] = x.keys[i]
        i -= 1
      x.keys[i + 1] = k
    else:
      while i >= 0 and k[0] < x.keys[i][0]:
        i -= 1
      i += 1
      if len(x.child[i].keys) == (2 * self.t) - 1:
        self.split_child(x, i)
        if k[0] > x.keys[i][0]:
          i += 1
      self.insert_non_full(x.child[i], k)

    # Split the child
  def split_child(self, node, idx):
    t = self.t
    y = node.child[idx]
    temp = BTreeNode(y.leaf)
    node.child.insert(idx + 1, temp)
    node.keys.insert(idx, y.keys[t - 1])
    temp.keys = y.keys[t: (2 * t) - 1]
    y.keys = y.keys[0: t - 1]
    if not y.leaf:
      temp.child = y.child[t: 2 * t]
      y.child = y.child[0: t - 1]


    # Delete a node
    def delete(self, node, k):
        t = self.t
        i = 0
        while i < len(node.keys) and k[0] > node.keys[i][0]:
            i += 1
        if node.leaf: # 리프노드라면?
            if i < len(node.keys) and node.keys[i][0] == k[0]: # 키를 찾으면 POP 그리고 리턴
                node.keys.pop(i)
                return
            return

        if i < len(node.keys) and node.keys[i][0] == k[0]: 
          #리프가 아닌데 키를 찾으면? 
          # delete_internal_node를 리턴
            return self.delete_internal_node(node, k, i)
        elif len(node.child[i].keys) >= t:
            self.delete(node.child[i], k)
        else:
            if i != 0 and i + 2 < len(node.child):
                if len(node.child[i - 1].keys) >= t:
                    self.delete_sibling(node, i, i - 1)
                elif len(node.child[i + 1].keys) >= t:
                    self.delete_sibling(node, i, i + 1)
                else:
                    self.delete_merge(node, i, i + 1)
            elif i == 0:
                if len(node.child[i + 1].keys) >= t:
                    self.delete_sibling(node, i, i + 1)
                else:
                    self.delete_merge(node, i, i + 1)
            elif i + 1 == len(node.child):
                if len(node.child[i - 1].keys) >= t:
                    self.delete_sibling(node, i, i - 1)
                else:
                    self.delete_merge(node, i, i - 1)
            self.delete(node.child[i], k)

    # Delete internal node
    def delete_internal_node(self, node, k, i):
        t = self.t
        if node.leaf:
            if node.keys[i][0] == k[0]:
                node.keys.pop(i)
                return
            return

        if len(node.child[i].keys) >= t:
            node.keys[i] = self.delete_predecessor(node.child[i])
            return
        elif len(node.child[i + 1].keys) >= t:
            node.keys[i] = self.delete_successor(node.child[i + 1])
            return
        else:
            self.delete_merge(node, i, i + 1)
            self.delete_internal_node(node.child[i], k, self.t - 1)

    # Delete the predecessor
    def delete_predecessor(self, x):
        if x.leaf:
            return x.pop()
        n = len(x.keys) - 1
        if len(x.child[n].keys) >= self.t:
            self.delete_sibling(x, n + 1, n)
        else:
            self.delete_merge(x, n, n + 1)
        self.delete_predecessor(x.child[n])

    # Delete the successor
    def delete_successor(self, x):
        if x.leaf:
            return x.keys.pop(0)
        if len(x.child[1].keys) >= self.t:
            self.delete_sibling(x, 0, 1)
        else:
            self.delete_merge(x, 0, 1)
        self.delete_successor(x.child[0])

    # Delete resolution
    def delete_merge(self, x, i, j):
        cnode = x.child[i]

        if j > i:
            rsnode = x.child[j]
            cnode.keys.append(x.keys[i])
            for k in range(len(rsnode.keys)):
                cnode.keys.append(rsnode.keys[k])
                if len(rsnode.child) > 0:
                    cnode.child.append(rsnode.child[k])
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child.pop())
            new = cnode
            x.keys.pop(i)
            x.child.pop(j)
        else:
            lsnode = x.child[j]
            lsnode.keys.append(x.keys[j])
            for i in range(len(cnode.keys)):
                lsnode.keys.append(cnode.keys[i])
                if len(lsnode.child) > 0:
                    lsnode.child.append(cnode.child[i])
            if len(lsnode.child) > 0:
                lsnode.child.append(cnode.child.pop())
            new = lsnode
            x.keys.pop(j)
            x.child.pop(i)

        if x == self.root and len(x.keys) == 0:
            self.root = new

    # Delete the sibling
    def delete_sibling(self, x, i, j):
        cnode = x.child[i]
        if i < j:
            rsnode = x.child[j]
            cnode.keys.append(x.keys[i])
            x.keys[i] = rsnode.keys[0]
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child[0])
                rsnode.child.pop(0)
            rsnode.keys.pop(0)
        else:
            lsnode = x.child[j]
            cnode.keys.insert(0, x.keys[i - 1])
            x.keys[i - 1] = lsnode.keys.pop()
            if len(lsnode.child) > 0:
                cnode.child.insert(0, lsnode.child.pop())



  # Print the tree
  def print_tree(self, x, l=0):
    print("Level ", l, " ", len(x.keys), end=":")
    for i in x.keys:
      print(i, end=" ")
    print()
    l += 1
    if len(x.child) > 0:
      for i in x.child:
        self.print_tree(i, l)

  # Search key in the tree
  def search_key(self, k, x=None):
    if x is not None:
      i = 0
      while i < len(x.keys) and k > x.keys[i][0]:
        i += 1
      if i < len(x.keys) and k == x.keys[i][0]:
        return (x, i)
      elif x.leaf:
        return None
      else:
        return self.search_key(k, x.child[i])
      
    else:
      return self.search_key(k, self.root)


def main():
  B = BTree(3)

  for i in range(10):
    B.insert((i, 2 * i))

  B.print_tree(B.root)

  if B.search_key(8) is not None:
    print("\nFound")
  else:
    print("\nNot Found")


if __name__ == '__main__':
  main()