# ctpbee_indicator
ctpbee里面实现的指标库, 能让你快速实现指标的计算和拿到值 

```python
  from indicator.interface import api
  close = api.open_csv('indicator/datas/orcl-2014.txt')
  api.update_bar(bar)
  # 简单移动平均线
  sma = api.sma()
  # 加权移动
  wma = api.wma()
  if close[-1] > sma[-1]:
      print("True")
      pass
  else:
      print("False")
      pass

```
