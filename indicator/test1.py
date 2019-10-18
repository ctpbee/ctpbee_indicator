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

close = show.open('./datas/orcl-2014.txt', '2014-01-01', '2014-12-31')
SMA = show.SimpleMovingAverage(close, 15)
WMA = show.WeightedMovingAverage(close, 25)
stdv = show.StandardDeviation(close)


def f(n):
    for i in n:
        yield i

g = f(SMA)



print(next(g))
print(g.__next__())
print(g.__next__())
print(g.__next__())
print(g.__next__())

show.plot()
