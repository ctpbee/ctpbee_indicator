import os
import sys
import datetime
import pandas as pd
import datetime
import numpy as np
import math
from copy import deepcopy


class indicator:
    pass

    # @property
    def open(self, file:str, startTime:str, endTime:str):
        """
        读取文件
        :param file: 文件名
        :param startTime: 开始读取时间
        :param endTime: 结束时间
        :return: dataframe对象
        """
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        # datapath = os.path.join(modpath, './datas/orcl-2014.txt')
        datapath = os.path.join(modpath, file)
        data = pd.read_csv(datapath, index_col=0, parse_dates=True)  # , index_col=0
        print(data, type(data))
        print(data['2014-01-01':'2014-01-08'])
        self.ret_data = data[startTime:endTime]
        return self.ret_data

    def sma(self, period:int, data:object):
        """
        简单移动平均线        print(self.lines[0].array, '++++++++++++++++++++++++++++++')
        :param period:距离
        :param data:数据 object
        :return:计算值
        """
        self.new_data = deepcopy(data)
        end = len(data['Close'])
        data = data['Close'].tolist()
        for i in range(period, end):
            self.new_data['Close'][i] = sum(data[i - period + 1:i + 1]) / period
        print(len(data), data)
        print(len(self.new_data), self.new_data['Close'])
        print(sum(self.new_data['Close'])/end)

    def calculate(self):
        """
        计算指标
        :return:
        """
        pass



s = indicator()
ret = s.open('./datas/orcl-2014.txt', '2014-01-01', '2014-12-31')
s.sma(15, ret)