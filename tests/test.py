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

