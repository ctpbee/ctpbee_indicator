# 平均数类
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..utils.py3 import with_metaclass

from . import Indicator


class MovingAverage(object):
    '''MovingAverage (alias MovAv)

    A placeholder to gather all Moving Average Types in a single place.

    Instantiating a SimpleMovingAverage can be achieved as follows::

      sma = MovingAverage.Simple(self.data, period)

    Or using the shorter aliases::

      sma = MovAv.SMA(self.data, period)

    or with the full (forwards and backwards) names:

      sma = MovAv.SimpleMovingAverage(self.data, period)

      sma = MovAv.MovingAverageSimple(self.data, period)
    移动平均值（别名movav）
    在一个地方收集所有移动平均值类型的占位符。
    实例化SimpleMovingAverage可以实现如下：
    SMA=移动平均值。简单（自数据，周期）
    或者使用较短的别名：
    SMA=移动平均SMA（自数据，周期）
    或者使用全名（向前和向后）：
    sma=movav.simplemovingAverage（自数据，周期）
    SMA=移动平均值简单（自数据，周期）
    '''
    _movavs = []

    @classmethod
    def register(cls, regcls):
        if getattr(regcls, '_notregister', False):
            return

        cls._movavs.append(regcls)

        clsname = regcls.__name__
        setattr(cls, clsname, regcls)

        clsalias = ''
        if clsname.endswith('MovingAverage'):
            clsalias = clsname.split('MovingAverage')[0]
        elif clsname.startswith('MovingAverage'):
            clsalias = clsname.split('MovingAverage')[1]

        if clsalias:
            setattr(cls, clsalias, regcls)


class MovAv(MovingAverage):
    pass  # alias


class MetaMovAvBase(Indicator.__class__):
    # Register any MovingAverage with the placeholder to allow the automatic
    # creation of envelopes and oscillators

    def __new__(meta, name, bases, dct):
        # Create the class
        cls = super(MetaMovAvBase, meta).__new__(meta, name, bases, dct)

        MovingAverage.register(cls)

        # return the class
        return cls


class MovingAverageBase(with_metaclass(MetaMovAvBase, Indicator)):
    params = (('period', 30),)
    plotinfo = dict(subplot=False)
