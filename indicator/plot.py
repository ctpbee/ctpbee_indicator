"""
    指标线
"""
from matplotlib import pyplot as plt
from indicator import indicator
import matplotlib.dates as mdate
import numpy as np
import pandas as pd


class ShowLine:
    def __init__(self):
        s = indicator()
        ret = s.open('./datas/orcl-2014.txt', '2014-01-01', '2014-12-31')
        SMA = s.SimpleMovingAverage(ret, 15)
        WMA = s.WeightedMovingAverage(ret, 25)

        time = s.ret_date

        # 一个画布
        fig = plt.figure(figsize=(8, 6))
        # 画布分块 块1
        ax1 = fig.add_subplot(211)
        # 柱
        ax1.bar(time, s.ret_volume, color='y')
        ax1.set_ylabel('volume')
        # 共用X轴
        ax2 = ax1.twinx()
        # 线
        ax2.plot(time, ret, "#000000", label="CLOSE")
        ax2.plot(time, SMA, "b", label="SMA")
        ax2.plot(time, WMA, "r", label="WMA")
        ax2.set_ylabel('price')
        # 标题
        plt.title("CTPBEE")
        # 网格
        plt.grid(True)
        # 图列
        plt.legend()


        # 块2
        pl2 = plt.subplot(212)
        # 柱形图
        plt.bar(time, s.ret_volume, color='y')
        # 网格
        plt.grid(True)
        plt.title("indicator")

        # 显示时间间隔
        ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d '))
        pl2.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d '))
        plt.show()


ShowLine()

