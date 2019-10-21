# -*- coding: utf-8 -*-
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



from plot import show

# close = show.open_json('./ctpbee_desktop/ag1911.SHFE.json', '2019-10-16', '2019-10-17')
close = show.open_csv('./datas/orcl-2014.txt', '2014-01-01')
SMA = show.SimpleMovingAverage(close, 15)
WMA = show.WeightedMovingAverage(close, 25)
stdv = show.StandardDeviation(close)

print(type(close))
# s = show.ret_data
# s.loc['2019-11-10'] = [1, 3,4,5, 5]
# print(s)
# print(s.Close)
if SMA[-1] > close[-1]:
    print("true")
else:
    print("false")

#
#
#
# print(next(g))
# print(g.__next__())
# print(g.__next__())
# print(g.__next__())
# print(g.__next__())
# n = (i for i in SMA)
# print(next(n))
# print(next(n))

show.plot()
