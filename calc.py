import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from cvxopt import matrix, solvers


class Stock(object):

    stock_name_list = [0]*50
    stock_dir_list = [0]*50
    daily_SD = [0]*50
    expect_RE = [0]*50
    cost = [0]*50
    whole_data=[[0]*50]*50

    def __init__(self):
        pass

    def load(self, path='./StockDir'):
        if not os.path.exists(path):
            raise ValueError

        self.stock_dir_list = os.listdir(path)
        for i, stock_name in enumerate(self.stock_dir_list):
            self.stock_name_list[i] = (stock_name.split('.ss')[0])

        for i, stock_dir in enumerate(self.stock_dir_list):
            raw_data = pd.read_csv('./StockDir/{}'.format(stock_dir), index_col='Date')
            #print(raw_data['Adj Close'][-1])
            self.whole_data[i] = raw_data['Adj Close'].values.tolist()
            self.daily_SD[i] = raw_data['Adj Close'].std()
            self.expect_RE[i] = (raw_data['Adj Close'][-1] - raw_data['Adj Close'][0])/raw_data['Adj Close'][0]
            self.cost[i] = raw_data['Adj Close'][-1]*100
        for i in np.argsort(self.expect_RE):
        	print(self.stock_dir_list[i])
        print(np.argsort(self.expect_RE))
        print(self.daily_SD)

def solve_modle(list_receive,value,list_SD,goals):
    #receive是每天的收盘价，value是增长率数列，SD是方差序列
    Q=2*matrix(np.array(list_receive.swapaxes(0,1).cov()))#.values.tolist())
    assert np.all(np.linalg.eigvals(np.array(Q)) > 0), '正定'
    #print(Q)
    p=matrix([0.0]*len(list_receive))
    G=matrix(- np.array(list_value)).T
    A=matrix(np.ones(len(value)),(1,len(value)))
    h=matrix([- goals])
    b=matrix(np.ones(1))
    print('Q:',Q,'p:',p,'G:',G,'h:',h,'A',A,'b:',b)
    sol=solvers.qp(Q,p,G,h,A,b)
    print(sol['x'])


ss = Stock()
ss.load()
#print(ss.whole_data[1])
l=np.argsort(ss.expect_RE)[::-1]
#print(ss.stock_dir_list[0][:-7])
tmp=[]
list_value=[]
list_SD=[]
for i in l[5:15]:
    tmp.append(ss.whole_data[int(l[i])])
    list_value.append(ss.expect_RE[int(l[i])])
    list_SD.append(ss.daily_SD[int(l[i])])
#print([ss.stock_dir_list[i][:-7] for i in l[:10]])
list_stock=pd.DataFrame(tmp)#,columns=[ss.stock_dir_list[i][:-7] for i in l[:10]])
print(list_stock.T.cov())#.values.tolist())
#print(np.array(- matrix(list_value)).T.shape)
solve_modle(list_stock,list_value,list_SD,0.2)
#print(np.array([- np.array(list_value),np.ones(len(list_value))]))
#print(list_stock.swapaxes(0,1).cov().tolist())




#print(ss.stock_dir_list[i][:-7])
#tmp=pd.DataFrame(ss.whole_data[int(l[i])],columns=[ss.stock_dir_list[0][:-7]])

#sh_return=pd.concat([ss.whole_data[30],ss.whole_data[34],ss.whole_data[38]],axis=1)
