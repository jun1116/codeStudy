from heapq import *
def mkgraph(costs):
    from collections import defaultdict
    dic=defaultdict(list)
    for fr,to,cost in costs:
        dic[fr].append([to,cost])
        dic[to]
    return dic

def dijkstra_v1(graph,start):
    INF=int(1e9)
    distances={i:INF for i in graph}
    frm={i:0 for i in graph}
    q=[]
    heappush(q, (0,start))
    distances[start]=0
    frm[start]=start

    while q:
        dist,now = heappop(q)
        if distances[now]<dist:continue
        for to,to_cost in graph[now]:
            cost=dist+to_cost
            if cost<distances[to]:
                distances[to]=cost
                frm[to]=now
                heappush(q,(cost,to))
    return distances, frm

def dijkstra_v2(graph,start):
    INF=int(1e9)
    distances={i:INF for i in graph}
    frm={i:0 for i in graph}
    q=[[0,start]]
    distances[start]=0
    frm[start]=start
    while q:
        dist,now=heappop(q)
        for to,to_cost in graph[now]:
            new_cost=dist+to_cost
            if new_cost<distances[to]:
                distances[to]=new_cost
                frm[to]=now
                heappush(q,[new_cost,to])
    return distances,frm

def route(graph,frm,start):
    for node in range(1,len(graph)+1):
        stk=[node]
        # stk.append(now)
        now=node
        while now!=start:
            now=frm.get(now)
            stk.append(now)
        # print(f'The Route To Node {node} : {stk}')
        print(f'The Route To Node {node} : {stk[::-1]}')



costs=[[1,2,2],[1,4,1],[1,3,5],[2,3,3],[2,4,2],[3,2,3],[3,6,5],[4,3,3],[4,5,1],[5,3,1],[5,6,2]]
graph=mkgraph(costs)
# print(dijkstra_v1(graph, 1))
distances,frm=dijkstra_v2(graph,1)
print(distances, frm)
route(graph,frm,1)

