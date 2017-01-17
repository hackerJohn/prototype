import numpy as np
from numpy import random as rm
import pandas as pd
#numpy 需要不是python的自带库
def simulation(T=4200):
    t = 0;nA =0;nD=0;n=0;A=[];D=[];N=[];S=[]
    tA = rm.exponential(10,1) # 数据包到来的时间
    tD = inf  # 数据包离开的时间
    while True:
        # print tA,tD,n,S
        if  (tA <= tD)  & (tA <= T): 
            t = tA 
            nA = nA + 1 # 更新数据包数
            n = n+1 # 保存服务系统中的用户（数据包）数量
            tA = t + rm.exponential(10,1) 
            if n==1: 
                tS = rm.uniform(5,10,1)
                tD = t + tS# 计算逗留时间
                S.append(tS) 
            A.append(t) # 保存时间序列        
        elif (tD <= tA) & (tD <=T): 
            t = tD; n= n-1
            nD = nD + 1
            if n==0:  tD = inf #如果无数据包等待
            else:  
                tS = rm.uniform(5,10,1)
                tD = t + tS
                S.append(tS) # 保存服务时间长度
            D.append(t) 
            N.append(n) 
        elif (tA>T) & (tD>T):  break 
    while True:
        if n <=0:  break
        t = tD;n=n-1;nD=nD+1 
        D.append(t) 
        N.append(n) 
        if n>0:
            tS = rm.uniform(5,10,1)
            tD = t +  tS
            S.append(tS) 
    Tp = max(t-T,0) 
    # A表示数据包来时点，D表示数据包离开时点，N表示系统中还有几个数据包，S表示服务时长
    raw = {'A':A,'D':D,'S':S,'N':N}
    data = pd.DataFrame(raw)
    return {'count': data.N.count(),'wcount':sum(data.N>0),'avgwait':float(mean(data.D-data.A-data.S))}

# 模拟100次，将结果存为dataframe
res = [simulation() for i in range(100)]
res = pd.DataFrame(res)
res

# 画出平均等待时间的直方图
import matplotlib.pyplot  as plt
plt.hist(res.avgwait)