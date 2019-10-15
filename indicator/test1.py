# import matplotlib.pyplot as plt
# from indicator import indicator
#
# s = indicator()
# ret = s.open('./datas/orcl-2014.txt', '2014-01-01', '2014-12-31')
# SMA = s.SimpleMovingAverage(ret, 15)
# WMA = s.WeightedMovingAverage(ret, 25)
#
# time = s.ret_date
#
# # 一个画布
# fig = plt.figure(figsize=(8, 6))
# # # x轴
# plt.xlabel("time")
# # y轴
# plt.ylabel("volume")
# # 线数据
# plt.plot(time, ret, "#000000", label="now")
# plt.plot(time, SMA, "b", label="SMA")
# plt.plot(time, WMA, "r", label="WMA")
#
# # 显示坐标轴
# plt.axis('on')
# # 显示网格
# plt.grid(True)
#
# # 添加图例
# plt.legend()
#
# # 展示
# plt.show()


# # -*- coding: utf-8 -*-
# from matplotlib.widgets import MultiCursor
# from pylab import figure, show, np
# t = np.arange(0.0, 2.0, 0.01)
# s1 = np.sin(2*np.pi*t)
# s2 = np.sin(4*np.pi*t)
# fig = figure()
# ax1 = fig.add_subplot(211)
# ax1.plot(t, s1)
# ax2 = fig.add_subplot(212, sharex=ax1)
# ax2.plot(t, s2)
# multi = MultiCursor(fig.canvas, (ax1, ax2), color='k', lw=1, vertOn=True, linestyle=':', horizOn=True, alpha=0.5)
# show()
from readfile import ReadFile
from indicator import Indicator
from plot import show

ret = ReadFile().open('./datas/orcl-2014.txt', '2014-01-01', '2014-12-31')
print(ret, '----')
print(dir(Indicator), Indicator().SimpleMovingAverage(ret, 15))
SMA = Indicator().SimpleMovingAverage(ret, 15)
WMA = Indicator().WeightedMovingAverage(ret, 25)
show().plot()