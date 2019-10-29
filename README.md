# ctpbee_indicator
ctpbee里面实现的指标库, 能让你快速实现指标的计算和拿到值 

```python
  from indicator.interface import api
  close = api.open_csv('indicator/datas/orcl-2014.txt')
  api.update_bar(bar)
  # 简单移动平均 
  sma = api.sma()
  # 加权移动平均
  wma = api.wma()
  # 指数移动平均
  ema = api.ema()
  # 随机指标
  k, d = api.kd()
  # 相对强度指数
  rsi = api.rsi()
  # 指数平滑移动平均线
  macd = api.macd()
  # 威廉指标
  wr = api.wr()
  # 布林带
  t, m, b = api.boll()
  
  smma = api.smma()
  # 真实平均范围
  atr = api.atr()
  # 标准偏差
  stdDev = api.stdDev()
  # 三重指数平滑移动平均
  trix = api.trix()
  # 变化率
  roc = api.roc()
  # 动量指标
  mtm = api.mtm()
  # 三式移动平均
  tema = api.tema()

  if close[-1] > sma[-1]:
      print("True")
      pass
  else:
      print("False")
      pass

```
