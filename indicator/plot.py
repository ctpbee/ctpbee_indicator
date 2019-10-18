"""
    指标线
"""
from matplotlib import pyplot as plt
from matplotlib.widgets import MultiCursor
from indicator import Indicator
import matplotlib.dates as mdate

colors = {
    "SimpleMovingAverage": "b",
    "ExponentialMovingAverage": "r",
    "WeightedMovingAverage": "c",
    "RSI": "g",
    "SmoothedMovingAverage": "r",
    "ATR": "w",
    "StandardDeviation": "k",
    "Trix": "c",
    "Momentum": "y",
    "TEMA": "m",
    "WilliamsR": "r",
    "MACDHisto": "g",
    "macd": "r",
    "signal": "b",
    "K": "g",
    "D": "r",
    "mid": "g",
    "top": "r",
    "bottom": "b"
}


class ShowLine(Indicator):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            obj = super(ShowLine, cls)
            cls._instance = obj.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()
        # self.count = indicator().count
        # self.ret_data = indicator().ret_data
        # self.ret_low = indicator().ret_low
        # self.ret_high = indicator().ret_high
        # self.ret_date = indicator().ret_date
        # self.ret_volume = indicator().ret_volume
        # self.ret_close = indicator().ret_close
        # self.average_message = indicator().average_message
        # self.indicator_message = indicator().indicator_message

        # s = File
        # ret = s.open('./datas/orcl-2014.txt', '2014-01-01', '2014-12-31')
        # SMA = indicator.SimpleMovingAverage(ret, 15)
        # WMA = indicator.WeightedMovingAverage(ret, 25)
        #
        # time = s.ret_date
        # # 一个画布
        # fig = plt.figure(figsize=(8, 6))
        # # 画布分块 块1
        # ax1 = fig.add_subplot(211)
        # # 柱
        # ax1.bar(time, s.ret_volume, color='y', label='volume')
        # ax1.set_ylabel('volume')
        # # 共用X轴
        # ax2 = ax1.twinx()
        # # 线
        # ax2.plot(time, ret, "#000000", label="CLOSE")
        # ax2.plot(time, SMA, "b", label="SMA")
        # ax2.plot(time, WMA, "r", label="WMA")
        # ax2.set_ylabel('price')
        # # 标题
        # plt.title("CTPBEE")
        # # 网格
        # plt.grid(True)
        # # 图列
        # plt.legend()
        #
        #
        # # 块2
        # pl2 = plt.subplot(212)
        # # 柱形图
        # plt.bar(time, s.ret_volume, color='y', label='volume')
        # # 网格
        # plt.grid(True)
        # plt.title("indicator")
        #
        # # 显示时间间隔
        # ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))  # %H:%M:%S
        # pl2.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))  # %H:%M:%S
        # plt.show()

    def plot(self, width=8, height=6, color="k", lw=0.5):
        # 一个画布
        fig = plt.figure(figsize=(width, height))
        # 画布分块 块1
        ax1 = fig.add_subplot(211)
        datetime = self.ret_date
        volume = self.ret_volume
        close = self.ret_close

        # 柱
        ax1.bar(datetime, volume, color='y', label='volume')
        ax1.set_ylabel('volume')
        ax2 = ax1.twinx()

        # 线
        ax2.plot(datetime, close, "#000000", label="CLOSE")
        for average_line in self.average_message:
            ax2.plot(datetime, self.average_message[average_line], colors[average_line], label=average_line)

        ax2.set_ylabel('price')
        # 标题
        plt.title("CTPBEE")
        # 网格
        plt.grid(True)
        # 图列
        plt.legend()
        # 显示时间间隔
        ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))  # %H:%M:%S

        # 块2
        ax3 = plt.subplot(212)
        # 柱形图
        for indicator_line in self.indicator_message:
            plt.plot(datetime, self.indicator_message[indicator_line], colors[indicator_line], label=indicator_line)
        # 网格
        plt.grid(True)
        plt.title("indicator")
        plt.legend()
        ax3.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))  # %H:%M:%S

        multi = MultiCursor(fig.canvas, (ax1, ax3), color=color, lw=lw, useblit=True, linestyle=':', horizOn=True)
        plt.show()


show = ShowLine()