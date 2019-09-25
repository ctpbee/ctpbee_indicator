from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    # 自定义价钱
    cerebro.broker.setcash(1000000.0)
    print("start value: %.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("final value: %.2f" % cerebro.broker.getvalue())