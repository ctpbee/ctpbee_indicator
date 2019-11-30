from indicator.plot import Scheduler


def inited():
    """
    用户判断是否满足计算指标
    :return: bool
    """
    return Scheduler.inited


def O():
    """
    Get open price time series.
    """
    return Scheduler.ret_open


def H():
    """
    Get high price time series.
    """
    return Scheduler.ret_high


def L():
    """
    Get low price time series.
    """
    return Scheduler.ret_low


def C():
    """
    Get low price time series
    :return:
    """
    return Scheduler.ret_close


def volume():
    """
    Get volume number
    :return:
    """
    return Scheduler.ret_volume


def open_csv(file: str, start_time=None, end_time=None):
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


def open_json(file: str, start_time=None, end_time=None):
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


def open_cache(data: list):
    """
    read CACHE data
        data_type:
            [["2014-01-01", 22, 44, 55, 55, 6666], ["2014-01-02", 22, 44, 55, 55, 6666], ...]
    :param data:
    :return:
    """
    return Scheduler.open_cache(data)


def add_bar(data, opens=False):
    """
    new bar push in array
    :param data: bar
    :param opens: if True save file  else not save (default False)
    :return:
    """
    Scheduler.update_bar(data, opens)


def MA(data, n=5):

    return Scheduler.ma(data, n)


def SMA(data, n=15):

    return Scheduler.sma(data, n)


def EMA(data, n=12, alpha=None):

    return Scheduler.ema(data, n, alpha)


def WMA(data, n=30):
    return Scheduler.wma(data, n)


def KD(data, n=14, f=3):
    return Scheduler.kd(data, n, f)


def MACD(data, n=12, m=20, f=9):
    return Scheduler.macd(data, n, m, f)


def RSI(data, n=14, l=1):
    return Scheduler.rsi(data, n, l)


def SMMA(data, n=10, alpha=15):
    return Scheduler.smma(data, n, alpha)


def ATR(data, n=14):
    return Scheduler.atr(data, n)


def STD(data, n=20):
    return Scheduler.stdDev(data, n)


def BOLL(data, n=20, m=2):
    return Scheduler.boll(data, n, m)


def TRIX(data, n=15, m=1):
    return Scheduler.trix(data, n, m)


def ROC(data, n=12):
    return Scheduler.roc(data, n)


def MTM(data, n=12):
    return Scheduler.mtm(data, n)


def TEMA(data, n=25):
    return Scheduler.tema(data, n)


def WR(data, n=14):
    return Scheduler.wr(data, n)


def CCI(n=20, f=0.015):
    return Scheduler.cci(n, f)


def SAR(data, n=2, af=0.02, afmax=0.20):
    return Scheduler.sar(data, n, af, afmax)


def HHV(data, n=10):
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


def LLV(data, n=10):
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


def REF(data, n=1):
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


def CROSS(K, D):
    """
    金叉 死叉
    :param K: 预信号
    :param D: 周转信号
    :return:
    """
    status = K - D
    return status


def SUM(data, n=7):
    return sum(data[-n:])


def ZIG(data, n):
    """
    转向率
    :param data: 0:开盘价,1:最高价,2:最低价,3:收盘价,其余:数组信息
    :param n: 变化率
    :return:
    """
    if data == 0:
        steering_rate = (Scheduler.ret_open[-1]-Scheduler.ret_open[-2])/Scheduler.ret_open[-2]*100
    elif data == 1:
        steering_rate = (Scheduler.ret_high[-1] - Scheduler.ret_high[-2]) / Scheduler.ret_high[-2] * 100
    elif data == 2:
        steering_rate = (Scheduler.ret_low[-1] - Scheduler.ret_low[-2]) / Scheduler.ret_low[-2] * 100
    elif data == 3:
        steering_rate = (Scheduler.ret_close[-1] - Scheduler.ret_close[-2]) / Scheduler.ret_close[-2] * 100
    else:
        steering_rate = (data[-1]-data[-2])/data[-2]
    if steering_rate > n:
        return True
    else:
        return False


def MIN(self):
    pass
