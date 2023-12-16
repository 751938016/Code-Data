import numpy as np
import pandas as pd
import copy
from random import shuffle as sl  
from random import randint as rd
import os  
import matplotlib.pyplot as plt
import networkx as nx
##################################################################
#################获取随机的有向无环图 并且检验是否是无环的###########
def random_graph(node,edge):
    '''返回邻接矩阵'''
    n = node
    node = range(0,n)   
    node = list(node)  
    
    sl(node)  #生成拓扑排序
    m = edge
    result = [] #存储生成的边，边用tuple的形式存储
    
    appeared_node = []
    not_appeared_node = node
    #生成前n - 1条边  
    while len(result) != n - 1:
    #生成第一条边
        if len(result) == 0:
            p1 = rd(0,n - 2)
            p2 = rd(p1+1,n - 1)
            x = node[p1]
            y = node[p2]
            appeared_node.append(x)
            appeared_node.append(y)
            not_appeared_node = list(set(node).difference(set(appeared_node)))
            result.append((x,y))
    #生成后面的边
        else:
            p1 = rd(0,len(appeared_node) - 1)
            x = appeared_node[p1]#第一个点从已经出现的点中选择
            p2 = rd(0,len(not_appeared_node) - 1)
            y = not_appeared_node[p2]
            appeared_node.append(y)#第二个点从没有出现的点中选择
            not_appeared_node = list(set(node).difference(set(appeared_node)))
    #必须保证第一个点的排序在第二个点之前
            if node.index(y) < node.index(x):
                result.append((y,x))
            else:
                result.append((x,y))
    #生成后m - n + 1条边     
    while len(result) != m:
        p1 = rd(0,n - 2)
        p2 = rd(p1+1,n - 1)
        x = node[p1]
        y = node[p2]
    #如果该条边已经生成过，则重新生成
        if (x,y) in result:
            continue
        else:
            result.append((x,y))
    
    matrix = np.zeros((n,n))
    for i in range(len(result)):
        matrix[result[i][0],result[i][1]] = 1

    return matrix



# 检验网络是否是无环的
class Graph(object):
    def __init__(self,G):
      self.G = G
      self.color = [0] * len(G)
      self.isDAG = True
           
    def DFS(self,i):
        self.color[i] = 1
        for j in range(len(self.G)):
            if self.G[i][j] != 0:
                if self.color[j] == 1:
                    self.isDAG = False
                elif self.color[j] == -1:
                    continue
                else:
                    # print('We are visiting node' + str(j + 1))
                    self.DFS(j)
        self.color[i] = -1
    #利用深度优先搜索判断一个图是否为DAG
    def DAG(self):
        for i in range(len(self.G)):
            if self.color[i] == 0:
                self.DFS(i)

##################################################################

# 对节点的入度和出度进行限制 保证网路的均匀性
def GetRandomLinksOnline(NumNodes,cross_degree,MaxInAndOut,LimitedInAndOut):
    '''返回键是因变量 值是自变量列表
        外生变量列表
        邻接矩阵'''
    Links = NumNodes*cross_degree
    # 生成邻接矩阵
    while 1:
        adj_martix = random_graph(NumNodes,Links)
        columns = np.sum(adj_martix,axis=0) #列的和
        rows = np.sum(adj_martix,axis=1) # 行的和
        Sum = columns+rows
        if LimitedInAndOut:
            if max(Sum) > MaxInAndOut:
                continue
            else:
                break
        else:
            break
    
    # 根据邻接矩阵获取连接字典
    # 键是因变量 值是自变量列表
    Networkslinks = dict()
    for i in range(adj_martix.shape[1]):
        Str2 = 'x' + str(i)
        Networkslinks[Str2] = list()

    for i in range(adj_martix.shape[0]):
        Str1 = 'x' + str(i)
        for j in range(adj_martix.shape[1]):
            Str2 = 'x' + str(j)
            if adj_martix[i][j] == 1:
                Networkslinks[Str2].append(Str1)

    # 生成外生变量列表 方便数据生成过程
    exvar = []
    for each in Networkslinks:
        if len(Networkslinks[each]) == 0: # 根据自回归生成外生变量的数值
            exvar.append(each) #保存外生变量的名称

    return Networkslinks,exvar,adj_martix

##################################################################
###########################数据计算过程############################

# 根据连接计算内生变量的值
def GetOutput(Input, Length, noise = 0.05): # 此处x是因变量，为了和获取自回归形式的函数相一致
    '''传入每一个因变量的自变量数据表 返回计算出的因变量的值和随机挑选的计算函数
       只是针对单个因变量进行的 在GetData中使用'''
    FunctionHome = ['X**2','X','np.exp(X)']
    # print(FunctionHome)
    # print(1)

    # 基准     ['X**2','X','np.exp(X)']             [0.4,0.4,0.2]
    
    # 修改之后的 使用相对简单的函数形式 不考虑二次方了 全部都是等可能的
    # cos      ['X','np.cos(X)']    
    # sqrt     ['X','X**0.5']      
    # log      ['X','np.log(X)']    
    # division ['X','1/X']        
    # all      ['X','1/X','np.log(X)','X**0.5','np.cos(X)','X**2','np.exp(X)'] 全部等可能
    OUTCalFunction = str() # 初始化计算函数，送给eval用
    OUTformation = str() # 初始化人类能理解的函数形式

    for EachInputName in Input.columns:
        OpationFunction = np.random.choice(FunctionHome,p=[0.4,0.4,0.2]) # ,p=[0.4,0.4,0.2]
        temp = copy.deepcopy(OpationFunction)
        CalculateInput = 'Input["'+EachInputName+'"]'
        OUTCalFunction = OUTCalFunction + temp.replace('X',CalculateInput) + '+'
        OUTformation = OUTformation + temp.replace('X',EachInputName) + '+'

    OUTCalFunction = OUTCalFunction[:-1]
    OUTformation = OUTformation[:-1]
    # print(OUTCalFunction)
    x = noise*np.random.rand(Length,1) #计算x时用到的噪声
    x += eval(OUTCalFunction).values.reshape(-1,1)
    #print(OUTCalFunction)
    return x, OUTformation

# 根据连接字典获取所有数据
def GetData(Networkslinks,exvar,Length,noise):
    '''传入连接字典 外生变量 样本长度 噪声 变量总数'''
    # 生成外生变量
    dfData = pd.DataFrame(np.random.rand(Length,len(exvar)),columns=exvar)
    HumanFun = dict()
    # 生成其他变量

    while 1:
        for eachOut in Networkslinks:
            if eachOut in dfData.columns:#如果已经在其中，则跳过
                pass
            else:#不在其中则计算，然后横向加入
                Input = copy.deepcopy(dfData)
                try:
                    Input = Input[Networkslinks[eachOut]] # 试图取变量，如果不是已知的，则到下一个
                except:
                    continue
                RelsutsOut, FunctionForm = GetOutput(Input, Length, noise)

                tempDF = pd.DataFrame(RelsutsOut,columns=[eachOut]) #获取因变量的值
                HumanFun[eachOut] = FunctionForm #获取计算方程的形式
                dfData = dfData.join(tempDF) 
            
        # break        
        if dfData.shape[1] == len(Networkslinks):
            break
    
    return HumanFun,dfData

##################################################################
###################绘制网络结构图并保存############################
def PlotNetwork(adj_martix,savepath,title):
    TempLinksDictforGraph = dict()
    TempLinksDictforGraph['from'] = list()
    TempLinksDictforGraph['to'] = list()
    for i in range(adj_martix.shape[0]):
        Str1 = 'x' + str(i)
        for j in range(adj_martix.shape[1]):
            Str2 = 'x' + str(j)
            # print(Str1+'->'+Str2)
            # print(adj_martix[i][j])
            if adj_martix[i][j] == 1:
                TempLinksDictforGraph['from'].append(Str1)
                TempLinksDictforGraph['to'].append(Str2)
    df = pd.DataFrame(TempLinksDictforGraph)
    G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())

    # 将绘制的图保存
    fig = plt.figure(figsize=(12,12))
    ax = plt.subplot(111)
    ax.set_title(title, fontsize=10)
    nx.draw_circular(G, with_labels=True, node_size=1500, alpha=0.3, arrows=True)
    plt.tight_layout()
    plt.savefig(savepath, format="PNG")
    plt.close()

# 建立一个文件夹
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path) 
    else: pass