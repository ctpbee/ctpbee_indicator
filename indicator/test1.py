import matplotlib.pyplot as plt
from indicator import indicator

s = indicator()
ret = s.open('./datas/orcl-2014.txt', '2014-01-01', '2014-12-31')
SMA = s.SimpleMovingAverage(ret, 15)
WMA = s.WeightedMovingAverage(ret, 25)

time = s.ret_date

# 一个画布
fig = plt.figure(figsize=(8, 6))
# # x轴
plt.xlabel("time")
# y轴
plt.ylabel("volume")
# 线数据
plt.plot(time, ret, "#000000", label="now")
plt.plot(time, SMA, "b", label="SMA")
plt.plot(time, WMA, "r", label="WMA")

# 显示坐标轴
plt.axis('on')
# 显示网格
plt.grid(True)

# 添加图例
plt.legend()

# 展示
plt.show()