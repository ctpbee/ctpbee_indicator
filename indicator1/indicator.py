import os
import sys
import datetime
import pandas as pd
import datetime
import numpy as np
import math
import operator
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
        # self.close_data = self.ret_data['Close']
        return self.ret_data

    def SimpleMovingAverage(self, data:object,  period=15):
        """
        简单移动平均线        print(self.lines[0].array, '++++++++++++++++++++++++++++++')
        :param period:距离
        :param data:数据 object
        :return:计算值
        """
        self.sma_data = deepcopy(data)
        end = len(data['Close'])
        close_line = data['Close'].tolist()
        for i in range(period, end):
            self.sma_data['Close'][i] = sum(close_line[i - period + 1:i + 1]) / period
        print(len(close_line), close_line)
        print(len(self.sma_data), self.sma_data['Close'].tolist())
        print(sum(self.sma_data['Close'])/end)
        return self.sma_data['Close']

    def sma(self):
        for c in self.ret_data['Close']:
            yield c

    def CloseValue(self):
        for i in self.sma_data['Close']:
            yield i

    def calculate(self):
        """
        计算指标
        :return:
        """
        pass

    def ExponentialMovingAverage(self, data:object, period:int, alpha=None):
        """
        指数移动平均
            - self.smfactor -> 2 / (1 + period)
            - self.smfactor1 -> `1 - self.smfactor`
            - movav = prev * (1.0 - smoothfactor) + newdata * smoothfactor
        :param data:
        :param period:
        :return:
        """
        self.ema_data = deepcopy(data)
        end = len(data['Close'])
        close_line = data['Close'].tolist()
        self.alpha = alpha
        if self.alpha is None:
            self.alpha = 2.0 / (1.0 + period)
        self.alpha1 = 1.0 - self.alpha

        prev = close_line[period-1]
        for i in range(period, end):
            self.ema_data['Close'][i] = prev = prev * self.alpha1 + close_line[i] * self.alpha
        print(len(close_line), close_line)
        print(self.ema_data['Close'].tolist())
        print(sum(self.ema_data['Close'][period:end]) / (end - period))
        return self.ema_data['Close']

    def WeightedMovingAverage(self, data:object, period=30):
        '''
        加权移动平均线
            A Moving Average which gives an arithmetic weighting to values with the
            newest having the more weight

            Formula:
              - weights = range(1, period + 1)
              - coef = 2 / (period * (period + 1))
              - movav = coef * Sum(weight[i] * data[period - i] for i in range(period))
            '''
        self.wma_data = deepcopy(data)
        end = len(data['Close'])
        close_line = data['Close'].tolist()
        coef = 2.0 / (period * (period + 1.0))
        weights = tuple(float(x) for x in range(1, period + 1))
        for i in range(period, end):
            data = close_line[i - period + 1: i + 1]
            self.wma_data['Close'][i] = coef * math.fsum(map(operator.mul, data, weights))
        print(len(close_line), close_line)
        print(self.wma_data['Close'].tolist())
        print(sum(self.wma_data['Close'][period:end])/(end-period))
        return self.wma_data['Close']


    def StochasticSlow(self, data:object, period:int):
        pass

    def MACDHisto(self, data:object, period_me1=12, period_me2=26, period_signal=9):
        """
        移动平均趋同/偏离
        Formula:
            - histo = macd - signal
        :param data:
        :param period:
        :return:
        """

        me1 = self.ExponentialMovingAverage(data, period=period_me1)
        me2 = self.ExponentialMovingAverage(data, period=period_me2)
        self.macd = me1 - me2
        self.signal = self.ExponentialMovingAverage(self.macd, period=period_signal)
        self.histo = self.macd - self.signal


    def RSI(self, data:object,  period:int):
        """
        相对强度指数
        Formula:
          - up = upday(data)
          - down = downday(data)
          - maup = movingaverage(up, period)
          - madown = movingaverage(down, period)
          - rs = maup / madown
          - rsi = 100 - 100 / (1 + rs)
        :param data:
        :param period:
        :return:
        """
        params = (
            ('period', 14),
            ('movav', MovAv.Smoothed),
            ('upperband', 70.0),
            ('lowerband', 30.0),
            ('safediv', False),
            ('safehigh', 100.0),
            ('safelow', 50.0),
            ('lookback', 1),
        )
        upday = UpDay(self.data, period=self.p.lookback)
        downday = DownDay(self.data, period=self.p.lookback)
        maup = self.p.movav(upday, period=self.p.period)
        madown = self.p.movav(downday, period=self.p.period)
        if not self.p.safediv:
            rs = maup / madown
        else:
            highrs = self._rscalc(self.p.safehigh)
            lowrs = self._rscalc(self.p.safelow)
            rs = DivZeroByZero(maup, madown, highrs, lowrs)

        self.lines.rsi = 100.0 - 100.0 / (1.0 + rs)

        rs = (-100.0 / (rsi - 100.0)) - 1.0
        return rs

    def SmoothedMovingAverage(self, data:object,  period:int, alpha=15):
        """
        smma 平滑移动平均值
        :param data:
        :param period:
        :return:
        """
        self.ema_data = deepcopy(data)
        end = len(data['Close'])
        close_line = data['Close'].tolist()
        self.alpha = alpha
        if self.alpha is None:
            self.alpha = 2.0 / (1.0 + period)
        self.alpha1 = 1.0 - self.alpha

        prev = close_line[period - 1]
        for i in range(period, end):
            self.ema_data['Close'][i] = prev = prev * self.alpha1 + close_line[i] * self.alpha
        print(len(close_line), close_line)
        print(self.ema_data['Close'].tolist())
        print(sum(self.ema_data['Close'][period:end]) / (end - period))
        return self.ema_data['Close']

    def ATR(self, data:object,  period:int):
        """
        平均真实范围
        AverageTrueRange
        :param data:
        :param period:
        :return:
        """
        pass

s = indicator()
ret = s.open('./datas/orcl-2014.txt', '2014-01-01', '2014-12-31')
s.SimpleMovingAverage(ret, 15)
s.WeightedMovingAverage(ret, 25)
s.WeightedMovingAverage(ret, 25)