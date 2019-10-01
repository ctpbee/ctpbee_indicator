from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import backtrader as bt
import backtrader.indicators as btind


class MyTest(bt.Strategy):
    params = (('period', 15),)

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        sma = btind.SMA(period=self.p.period)

    def next(self):
        ltxt = '%d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f'

        self.log(ltxt %
                 (len(self),
                  self.data.open[0], self.data.high[0],
                  self.data.low[0], self.data.close[0],
                  self.data.volume[0], self.data.openinterest[0]))