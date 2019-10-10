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
        self.ret_data = data[startTime:endTime]
        # self.close_data = self.ret_data['Close']
        self.ret_low = self.ret_data['Low']
        self.ret_high = self.ret_data['High']
        return self.ret_data['Close']

    def SimpleMovingAverage(self, data:object,  period=15):
        """
        sma
        简单移动平均线
        :param period:距离
        :param data:数据 object
        :return:计算值
        """
        self.sma_data = deepcopy(data)
        end = len(data)
        close_line = data
        for i in range(period, end):
            self.sma_data[i] = sum(close_line[i - period + 1:i + 1]) / period
        return self.sma_data

    def sma(self):
        for c in self.ret_data:
            yield c

    def CloseValue(self):
        for i in self.sma_data:
            yield i

    def calculate(self):
        """
        计算指标
        :return:
        """
        pass

    def ExponentialMovingAverage(self, data:object, period:int, alpha=None):
        """
        ema
        指数移动平均
            - self.smfactor -> 2 / (1 + period)
            - self.smfactor1 -> `1 - self.smfactor`
            - movav = prev * (1.0 - smoothfactor) + newdata * smoothfactor
        :param data:
        :param period:
        :return:
        """
        self.ema_data = deepcopy(data)
        end = len(data)
        close_line = data
        self.alpha = alpha
        if self.alpha is None:
            self.alpha = 2.0 / (1.0 + period)
        self.alpha1 = 1.0 - self.alpha

        prev = close_line[period-1]
        for i in range(period, end):
            self.ema_data[i] = prev = prev * self.alpha1 + close_line[i] * self.alpha
        return self.ema_data

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
        end = len(data)
        close_line = data
        coef = 2.0 / (period * (period + 1.0))
        weights = tuple(float(x) for x in range(1, period + 1))
        for i in range(period, end):
            data = close_line[i - period + 1: i + 1]
            self.wma_data[i] = coef * math.fsum(map(operator.mul, data, weights))
        return self.wma_data

    def StochasticSlow(self, data:object, period:int, period_dfast=3):
        """
        随机振荡器
            The regular (or slow version) adds an additional moving average layer and
            thus:

              - The percD line of the StochasticFast becomes the percK line
              - percD becomes a  moving average of period_dslow of the original percD

            Formula:
              - k = k
              - d = d
              - d = MovingAverage(d, period_dslow)
            :param data:
            :param period:
            :return:
        """
        highest = max(self.ret_high[period:])
        lowest = min(self.ret_low[period:])
        knum = np.array(data[period:]) - lowest
        kden = highest - lowest
        self.k = 100 * (knum/kden)
        self.k = [0]*period+self.k.tolist()
        self.d = self.SmoothedMovingAverage(self.k, period=period_dfast)
        self.stochastic = self.SimpleMovingAverage(self.d, period=period_dfast)
        print('====', self.stochastic)
        return self.stochastic

    def MACDHisto(self, data:object, period_me1=12, period_me2=26, period_signal=9):
        """
        移动平均趋同/偏离
        Formula:
            - macd = ema(data, me1_period) - ema(data, me2_period)
            - signal = ema(macd, signal_period)
            - histo = macd - signal
        :param data:
        :param period:
        :return:
        """

        me1 = self.ExponentialMovingAverage(data, period=period_me1)
        me2 = self.ExponentialMovingAverage(data, period=period_me2)
        self.macd = np.array(me1) - np.array(me2)
        self.signal = self.ExponentialMovingAverage(self.macd.tolist(), period=period_signal)
        self.histo = np.array(self.macd) - np.array(self.signal)
        return self.histo.tolist()

    def RSI(self, data:object,  period:int, lookback=1):
        """
        rsi 相对强度指数
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
            ('upperband', 70.0),
            ('lowerband', 30.0),
            ('safediv', False),
            ('safehigh', 100.0),
            ('safelow', 50.0),
            ('lookback', 1),
        )
        end = len(data)
        upday = []
        downday = []
        upday = upday + [0] * period
        for i in range(period+1, end):
            upday.append(max(data[i]-data[i-1], 0.0))
        downday = downday + [0] * period
        for i in range(period+1, end):
            downday.append(max(data[i-1]-data[i], 0.0))
        maup = self.SmoothedMovingAverage(upday, period=period)
        madown = self.SmoothedMovingAverage(downday, period=period)
        rs = np.array(maup) / np.array(madown)
        rsi_list = []
        for i in rs:
            rsi = 100.0 - 100.0 / (1.0 + i)
            rsi_list.append(rsi)
        print(rsi_list, '----------')
        return rsi_list

    def SmoothedMovingAverage(self, data:object,  period:int, alpha=15):
        """
        smma 平滑移动平均值
        SmoothedMovingAverage
        :param data:
        :param period:
        :return:
        """
        self.ema_data = deepcopy(data)
        end = len(data)
        close_line = data
        self.alpha = alpha
        if self.alpha is None:
            self.alpha = 2.0 / (1.0 + period)
        self.alpha1 = 1.0 - self.alpha

        prev = close_line[period - 1]
        for i in range(period, end):
            self.ema_data[i] = prev = prev * self.alpha1 + close_line[i] * self.alpha
        return self.ema_data

    def ATR(self, data:object,  period:int):
        """
        平均真实范围
        AverageTrueRange
        :param data:
        :param period:
        :return:
        """
        truehigh = []
        truelow = []
        end = len(data)
        truehigh = truehigh + [0] * period
        for h in range(period+1, end):
            truehigh.append(max(data[h-1], self.ret_high[h]))
        truelow = truelow + [0] * period
        for l in range(period+1, end):
            truelow.append(min(data[l-1], self.ret_low[l]))
        tr = np.array(truehigh) - np.array(truelow)
        atr = self.SimpleMovingAverage(tr, period=period)
        return atr

    def BollingerBands(self, data:object, period:int):
        """
        布林带
        Formula:
          - midband = SimpleMovingAverage(close, period)
          - topband = midband + devfactor * StandardDeviation(data, period)
          - botband = midband - devfactor * StandardDeviation(data, period)

        See:
          - http://en.wikipedia.org/wiki/Bollinger_Bands
        :param data:
        :param period:
        :return:
        """

    def AroonIndicator(self, data:object, period:int):
        """
        Formula:
          - up = 100 * (period - distance to highest high) / period
          - down = 100 * (period - distance to lowest low) / period
        See:
            - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:aroon
        :param data:
        :param period:
        :return:
        """

    def UltimateOscillator(self, data: object, period: int):
        '''
            Formula:
              # Buying Pressure = Close - TrueLow
              BP = Close - Minimum(Low or Prior Close)

              # TrueRange = TrueHigh - TrueLow
              TR = Maximum(High or Prior Close)  -  Minimum(Low or Prior Close)

              Average7 = (7-period BP Sum) / (7-period TR Sum)
              Average14 = (14-period BP Sum) / (14-period TR Sum)
              Average28 = (28-period BP Sum) / (28-period TR Sum)

              UO = 100 x [(4 x Average7)+(2 x Average14)+Average28]/(4+2+1)

            See:

              - https://en.wikipedia.org/wiki/Ultimate_oscillator
              - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ultimate_oscillator
        '''
        pass

    def Trix(self, data: object, period: int, rocperiod=1):
        '''
            技术分析
           Defined by Jack Hutson in the 80s and shows the Rate of Change (%) or slope
           of a triple exponentially smoothed moving average

           Formula:
             - ema1 = EMA(data, period)
             - ema2 = EMA(ema1, period)
             - ema3 = EMA(ema2, period)
             - trix = 100 * (ema3 - ema3(-1)) / ema3(-1)

             The final formula can be simplified to: 100 * (ema3 / ema3(-1) - 1)

           The moving average used is the one originally defined by Wilder,
           the SmoothedMovingAverage

           See:
             - https://en.wikipedia.org/wiki/Trix_(technical_analysis)
             - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:trix
        '''
        ema1 = self.ExponentialMovingAverage(data, period=period)
        ema2 = self.ExponentialMovingAverage(ema1, period=period)
        ema3 = self.ExponentialMovingAverage(ema2, period=period)
        self.trix = 100.0 * (np.array(ema3)/ema3[-rocperiod] - 1.0)
        print(self.trix)
        return self.trix

    def ROC(self, data: object, period: int):
        pass

    def Momentum(self, data: object, period: int):
        pass

    def DMA(self, data: object, period: int):
        pass

    def TEMA(self, data: object, period: int):
        pass
s = indicator()
ret = s.open('./datas/orcl-2014.txt', '2014-01-01', '2014-12-31')
s.SimpleMovingAverage(ret, 15)
s.WeightedMovingAverage(ret, 25)
# s.RSI(ret, 14)
# s.ATR(ret, 14)
# s.StochasticSlow(ret, 14)
s.Trix(ret, 15)