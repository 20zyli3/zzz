import numpy as np
import networkx as nx
import random
from random import choice

def read_graph(filename=None, separator=None):
    fname = filename
    # graph = nx.read_edgelist(fname, delimiter=',', nodetype=int)
    graph = nx.read_edgelist(fname, delimiter=separator, nodetype=int)
    # print(graph)
    # graph = graph.to_undirected()
    return graph, fname.split('/')[-1]
def find_max_connected(path=None):
    G,fname=read_graph(path)
    print('原网络大小:',G)
    print('原网络连通分量',nx.number_connected_components(G))
    for c in nx.connected_components(G):
        t1 = G.subgraph(c)
        print(t1)
        if 10000>t1.number_of_nodes():
             print(t1)
             break
    return t1

def read_graph2(filename=None, separator=None):
    fname = filename
    graph = nx.read_edgelist(fname, delimiter=separator, nodetype=float)
    print('预备删边网络的大小',graph)
    graph = graph.to_undirected()
    return graph, fname.split('/')[-1]

def delete_edges(graph=None,graphf=None,rate=None):
    delete_edges_num=int(rate*nx.number_of_edges(graph)) # 删除边的数量
    number_connected=nx.number_connected_components(graph)#获取图的连通分量
    list_1 =[]
    for i in range(delete_edges_num):
        while(list_1!=list(graphf.edges)):# 防止所有的边删去的可能性试完，也没有达到20%删边的要求
            num1 =choice(list(graphf.edges))#从副本中任选一条边，
            if num1 in list(graphf.edges):#G和G的副本F中尝试删除任选的边，若G的连通连通分量不变，则在G中删除该边，并跳出循环，否则加回原本删去的边,重新随机删边
                graphf.remove_edge(num1[0],num1[1])#建立副本F的原因是避免随机删边重复
                graph.remove_edge(num1[0], num1[1])#G也进行删边，如果删边后连通分量改变，则加回该边，若删边后不改变，则就此删除该边并继续循环
                if(nx.number_connected_components(graph)==number_connected):
                    break
                else:
                    graph.add_edge(num1[0], num1[1])
                    continue
            else:
                continue
        print(nx.number_of_edges(G))
    return graph

data_path='dataset/com-youtube.ungraph.txt/com-youtube.ungraph.txt'
new_datapath="dataset/new_brightkite.txt"
new_datapath_delete="dataset/new_brightkite_delete.txt"
rate=0.2#删边的比率

max_connected=find_max_connected(data_path)
print('新网络大小',max_connected)
np.savetxt(new_datapath, max_connected.edges(), delimiter=" ")
print('新网络的连通分量',nx.number_connected_components(max_connected))
print('新网络的连通性',nx.is_connected(max_connected))

G,fname_b=read_graph2(filename=new_datapath)
F,fname_b2=read_graph2(filename=new_datapath)
E,fname_b3=read_graph2(filename=new_datapath)
K=delete_edges(G,F,rate)
np.savetxt(new_datapath_delete, K.edges, delimiter=" ")
print('删边后网络的大小',K)
print('删边后网络的连通分量',nx.number_connected_components(K))
print('删边后网络的连通性:',nx.is_connected(K))
# print(set(K.edges()))
# print(set(E.edges()))
# 验证，删边后的边集合是否为原图的边集合的子集
print('验证删边后的网络是否为删边前的子集:',set(E.edges())>set(K.edges()))#数组转换为集合进行比较