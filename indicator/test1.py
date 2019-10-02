import os
import sys
import datetime
import pandas as pd
import datetime
import numpy as np
import math


class indicator:
    pass

    @property
    def open(self, file:str, startTime:str, endTime:str):
        """
        读取文件
        :param file: 文件名
        :param startTime: 开始读取时间
        :param endTime: 结束时间
        :return: framedata对象
        """
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        # datapath = os.path.join(modpath, './datas/orcl-2014.txt')
        datapath = os.path.join(modpath, file)
        data = pd.read_csv(datapath, index_col=0, parse_dates=True)  # , index_col=0
        print(data, type(data))
        print(data['2014-01-03':'2014-01-08'])
        # for i in data['Open']:
        #     print(i)
        ret_data = data[startTime:endTime]
        return ret_data

    def MovingAverageSimple(self, period:int, data):
        """
        简单移动平均线
        :param period:距离
        :param data:数据 objec
        :return:计算值
        """
        math.fsum()
s = indicator()
s.open