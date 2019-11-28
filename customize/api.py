from indicator.plot import Scheduler


class Indicator:

    @property
    def inited(self):
        """
        用户判断是否满足计算指标
        :return: bool
        """
        return Scheduler.inited

    @property
    def O(self):
        """
        Get open price time series.
        """
        return Scheduler.ret_open

    @property
    def H(self):
        """
        Get high price time series.
        """
        return Scheduler.ret_high

    @property
    def L(self):
        """
        Get low price time series.
        """
        return Scheduler.ret_low

    @property
    def C(self):
        """
        Get low price time series
        :return:
        """
        return Scheduler.ret_close

    @property
    def volume(self):
        """
        Get volume number
        :return:
        """
        return Scheduler.ret_volume

    def open_csv(self, file: str, start_time=None, end_time=None):
        """
        open TXT file
            data_type:
                Date,Open,High,Low,Close,Volume
                '2019-01-07 00:00:00', 3831.0, 3847.0, 3831.0, 3840.0, 554
                '2019-01-08 00:00:00', 3841.0, 3841.0, 3833.0, 3836.0, 554
                ...
        :param file: name
        :param start_time:
        :param end_time:
        :return:
        """
        return Scheduler.open_csv(file, start_time, end_time)

    def open_json(self, file: str, start_time=None, end_time=None):
        """
        open JSON file
            data_type:
                {"zn1912.SHFE": [
                        ["2014-01-01", 18780.0, 18780.0, 18770.0, 18775.0, 266],
                        ["2014-01-02", 18775.0, 18780.0, 18770.0, 18770.0, 312],
                            ...
                        ]
                }
        :param file: name
        :param start_time:
        :param end_time:
        :return:
        """
        return Scheduler.open_json(file, start_time, end_time)

    def open_cache(self, data: list):
        """
        read CACHE data
            data_type:
                [["2014-01-01", 22, 44, 55, 55, 6666], ["2014-01-02", 22, 44, 55, 55, 6666], ...]
        :param data:
        :return:
        """
        return Scheduler.open_cache(data)

    def add_bar(self, data, opens=False):
        """
        new bar push in array
        :param data: bar
        :param opens: if True save file  else not save (default False)
        :return:
        """
        Scheduler.update_bar(data, opens)

    def MA(self, data, n=5):
        if not self.inited:
            return
        return Scheduler.ma(data, n)

    def SMA(self, data, n=15):
        if not self.inited:
            return
        return Scheduler.sma(data, n)

    def EMA(self, data, n=12, alpha=None):
        if not self.inited:
            return
        return Scheduler.ema(data, n, alpha)

    def WMA(self, data, n=30):
        if not self.inited:
            return
        return Scheduler.wma(data, n)

    def KD(self, data, n=14, f=3):
        if not self.inited:
            return
        return Scheduler.kd(data, n, f)

    def MACD(self, data, n=12, m=20, f=9):
        if not self.inited:
            return
        return Scheduler.macd(data, n, m, f)

    def RSI(self, data, n=14, l=1):
        if not self.inited:
            return
        return Scheduler.rsi(data, n, l)

    def SMMA(self, data, n=10, alpha=15):
        if not self.inited:
            return
        return Scheduler.smma(data, n, alpha)

    def ATR(self, data, n=14):
        if not self.inited:
            return
        return Scheduler.atr(data, n)

    def STD(self, data, n=20):
        if not self.inited:
            return
        return Scheduler.stdDev(data, n)

    def BOLL(self, data, n=20, m=2):
        if not self.inited:
            return
        return Scheduler.boll(data, n, m)

    def TRIX(self, data, n=15, m=1):
        if not self.inited:
            return
        return Scheduler.trix(data, n, m)

    def ROC(self, data, n=12):
        if not self.inited:
            return
        return Scheduler.roc(data, n)

    def MTM(self, data, n=12):
        if not self.inited:
            return
        return Scheduler.mtm(data, n)

    def TEMA(self, data, n=25):
        if not self.inited:
            return
        return Scheduler.tema(data, n)

    def WR(self, data, n=14):
        if not self.inited:
            return
        return Scheduler.wr(data, n)

    def CCI(self, n=20, f=0.015):
        if not self.inited:
            return
        return Scheduler.cci(n, f)

    def SAR(self, data, n=2, af=0.02, afmax=0.20):
        if not self.inited:
            return
        return Scheduler.sar(data, n, af, afmax)

    def HHV(self, data, n=10):
        """
        在一定周期内某一项数据的最大值
        :param data:
        :param n:
        :return:
        """
        if data.lower() == "l" or data.lower() == "low":
            return max(Scheduler.ret_low[-1 - n:])
        elif data.lower() == "v" or data.lower() == "volume":
            return max(Scheduler.ret_volume[-1 - n:])
        elif data.lower() == "h" or data.lower() == "high":
            return max(Scheduler.ret_high[-1 - n:])
        elif data.lower() == "c" or data.lower() == "close":
            return max(Scheduler.ret_close[-1 - n:])
        else:
            return max(data[-1 - n:])

    def LLV(self, data, n=10):
        """
        在一定周期内某一项数据的最小值
        :param data:
        :param n:
        :return:
        """
        if data.lower() == "l" or data.lower() == "low":
            return min(Scheduler.ret_low[-1 - n:])
        elif data.lower() == "v" or data.lower() == "volume":
            return min(Scheduler.ret_volume[-1 - n:])
        elif data.lower() == "h" or data.lower() == "high":
            return min(Scheduler.ret_high[-1 - n:])
        elif data.lower() == "c" or data.lower() == "close":
            return min(Scheduler.ret_close[-1 - n:])
        else:
            return min(data[-1 - n:])

    def REF(self, data, n=1):
        """
        昨日收盘价 ref(c,1)表示昨天的收盘价, ref(v,1)表示昨天的成交量
        :param data:
        :param n:
        :return:
        """
        if data.lower() == "l" or data.lower() == "low":
            return Scheduler.ret_low[-1 - n]
        elif data.lower() == "v" or data.lower() == "volume":
            return Scheduler.ret_volume[-1 - n]
        elif data.lower() == "h" or data.lower() == "high":
            return Scheduler.ret_high[-1 - n]
        elif data.lower() == "c" or data.lower() == "close":
            return Scheduler.ret_close[-1 - n]
        else:
            return data[-1 - n]

    def CROSS(self, K, D):
        """
        金叉 死叉
        :param K: 预信号
        :param D: 周转信号
        :return:
        """
        status = K - D
        return status

    def SUM(self, data, n=7):
        return sum(data[-n:])

    def ZIG(self, data, n):

        pass

    def MIN(self):
        pass
