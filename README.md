# ctpbee_indicator
ctpbee里面实现的指标库, 能让你快速实现指标的计算和拿到值 

```python
  from indicator.plot import Cerebro
  close = Cerebro.open_csv('indicator/datas/orcl-2014.txt', '2014-01-01')
  Cerebro.update_bar(bar)
  # 简单移动平均线
  sma = Cerebro.sma(close, 15)
  # 加权移动
  wma = Cerebro.wma(close, 25)
  if close[-1] > sma[-1]:
      print("True")
      pass
  else:
      print("False")
      pass

```
