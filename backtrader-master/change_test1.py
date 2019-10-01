import backtrader as bt
import os, sys
import pandas as pd
import datetime

modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, './datas/orcl-2014.txt')

dataframe = pd.read_csv(datapath, index_col=0, parse_dates=True)
print(dataframe, '-----------------------')
dataframe['openinterest'] = 0
datas = bt.feeds.PandasData(dataname=dataframe,
                           fromdate=datetime.datetime(2014, 1, 1),
                           todate=datetime.datetime(2014, 12, 31))
print(datas)
sma = bt.indicators.SimpleMovingAverage(
            datas, period=15)

# print("%s, %s, %s, %s, %s" % (datas[0].open[0], datas[0].high[0], datas[0].low[0], datas[0].close[0], datas[0].volume))
print(sma, '................................')