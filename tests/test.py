from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np

np.seterr(all='ignore')
rcParams['figure.figsize'] = (14, 6)

from funcat import *

from funcat.data.tushare_backend import TushareDataBackend
from funcat.data.rqalpha_data_backend import RQAlphaDataBackend

backend = "tushare"

if backend == "rqalpha":
    set_data_backend(RQAlphaDataBackend("~/.rqalpha/bundle"))
elif backend == "tushare":
    set_data_backend(TushareDataBackend())

set_start_date("2015-01-01")
S("000001.XSHG")  # 设置当前关注股票
T("2016-06-01")   # 设置当前观察日期

print(O, H, L, C, V)
print(C / C[1] - 1)



##############
#    通达信   #
#            #
##############

O: 开盘价
C: 收盘价
H: 最高价
L: 最低价

#  昨日收盘价 ref(c,1)表示昨天的收盘价, ref(v,1)表示昨天的成交量
REF(c, 1)

# 字转向函数 ZIG(K,N),当价格变化量超过N%时转向,K表示0:开盘价,1:最高价,2:最低价,3:收盘价,其
ZIG(K, N)

# 在一定周期内某一项数据的最大值
HHV(H, 10)

# 在一定周期内某一项数据的最小值
LLV(H, 10)

# 增幅
(C-REF(C, 1))/REF(C, 1)*100

# 振幅
(H-L)/L*100

# 均价
(H+L+O+C)/4

# 均价
AMOUNT/(V*100)

# 振幅
DYNAINFO(12)*100


# CROSS 是否发生交叉

K1: KDJ.K
D1: KDJ.D

# 金叉
CROSS(K1, D1)*10
# 死叉
CROSS(D1, K1)*-10

# 上次到现的周期数
BARSLAST(金叉)

# 首次到现周期数
BARSSINCE(金叉), NODRAW

# 连涨
UPNDAY(C, 5)

# 连跌
DOWNNDAY(C, 5)