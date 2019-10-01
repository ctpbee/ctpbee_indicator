import os
import sys
import datetime
import pandas as pd
import datetime
import numpy as np


class indicator:
    pass

    @property
    def open(self):
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        datapath = os.path.join(modpath, './datas/orcl-2014.txt')
        data = pd.read_csv(datapath, index_col=0, parse_dates=True)  # , index_col=0
        print(data, type(data))
        print(data['2014-01-03':'2014-01-08'])
        # for i in data['Open']:
        #     print(i)
        sma = '888'
        print(sma)
s = indicator()
s.open