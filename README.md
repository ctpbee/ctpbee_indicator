# ctpbee_indicator
ctpbee里面实现的指标库, 能让你快速实现指标的计算和拿到值 

```python
  from indicator.interface import api
  info = api()
  bar_3 = info.open_csv('indicator/datas/orcl-2014.txt')
 
  def on_bar(self, bar):
      # opens是否要保存数据(默认false不保存)
      info.add_bar(bar)
      close_price = info.close
      # 简单移动平均  默认 15
      sma = info.sma()
      # 加权移动平均  默认30
      wma = info.wma()
      # 指数移动平均 默认12
      ema = info.ema()
      # 随机指标 默认参数 14, 3
      k, d = info.kd()
      # 相对强度指数 默认 14, 1
      rsi = info.rsi()
      # 异同移动平均线 默认 12, 20, 9
      macd, signal, histo = info.macd()
      # 威廉指标 默认 14
      wr = info.wr()
      # 布林带 默认 20 2
      t, m, b = info.boll()
      # 默认 10, 15
      smma = info.smma()
      # 真实平均范围 默认 14
      atr = info.atr()
      # 标准偏差 默认 20
      stdDev = info.stdDev()
      # 三重指数平滑移动平均 默认 15, 1
      trix = info.trix()
      # 变化率 默认 12
      roc = info.roc()
      # 动量指标 默认 12
      mtm = info.mtm()
      # 三式移动平均 默认 25
      tema = info.tema()
    
      if close_price[-1] > sma[-1]:
          print("True")
          pass
      else:
          print("False")
          pass

```
# example(简单列子)

例子一 
```python
import json
from datetime import datetime, date
from ctpbee import LooperApi, Vessel
from ctpbee.constant import Direction
from indicator.interface import api


def get_data(start, end, symbol, exchange, level):
    """ using rqdatac to make an example """
    # import rqdatac as rq
    # from rqdatac import get_price, id_convert
    # username = "license"
    # password = "NK-Ci7vnLsRiPPWYwxvvPYdYM90vxN60qUB5tVac2mQuvZ8f9Mq8K_nnUqVspOpi4BLTkSLgq8OQFpOOj7L" \
    #            "t7AbdBZEBqRK74fIJH5vsaAfFQgl-tuB8l03axrW8cyN6-nBUho_6Y5VCRI63Mx_PN54nsQOpc1psIGEz" \
    #            "gND8c6Y=bqMVlABkpSlrDNk4DgG-1QXNknJtk0Kkw2axvFDa0E_XPMqOcBxifuRa_DFI2svseXU-8A" \
    #            "eLjchnTkeuvQkKh6nrfehVDiXjoMeq5sXgqpbgFAd4A5j2B1a0gpE3cb5kXb42n13fGwFaGris" \
    #            "8-eKzz_jncvuAamkJEQQV0aLdiw="
    # host = "rqdatad-pro.ricequant.com"
    # port = 16011
    # rq.init(username, password, (host, port))
    # symbol_rq = id_convert(symbol)
    # data = get_price(symbol_rq, start_date=start, end_date=end, frequency=level, fields=None,
    #                  adjust_type='pre', skip_suspended=False, market='cn', expect_df=False)
    # origin = data.to_dict(orient='records')
    # result = []
    # for x in origin:
    #     do = {}
    #     do['open_price'] = x['open']
    #     do['low_price'] = x['low']
    #     do['high_price'] = x['high']
    #     do['close_price'] = x['close']
    #     do['datetime'] = datetime.strptime(str(x['trading_date']), "%Y-%m-%d %H:%M:%S")
    #     do['symbol'] = symbol
    #     do['local_symbol'] = symbol + "." + exchange
    #     do['exchange'] = exchange
    #     result.append(do)
    # return result

def get_a_strategy():

    class SmaStrategy(LooperApi):

        def __init__(self, name):
            super().__init__(name)
            self.count = 1
            self.pos = 0

            self.bar_3 = api()  # 3分钟bar线
            self.bar_3.open_json('indicator/json/zn1912.SHFE.json')  # 读取本地数据

            self.allow_max_price = 5000  # 设置价格上限 当价格达到这个就卖出 防止突然跌
            self.allow_low_price = 2000  # 设置价格下限 当价格低出这里就卖 防止巨亏

        def on_bar(self, bar):
            # todo: 收盘连长
            """ """
            self.bar_3.add_bar(bar)
            close = self.bar_3.close

            if self.allow_max_price < close[-1] and self.pos > 0:
                self.action.sell(bar.close_price, self.pos, bar)

            if self.allow_low_price > close[-1] and self.pos > 0:
                self.action.sell(bar.close_price, self.pos, bar)

            # 接连三天涨
            if close[-1] > close[-2] > close[-3]:
                # 没有就买
                if self.pos == 0:
                    self.action.buy(bar.close_price, 1, bar)
                
        def on_trade(self, trade):
            if trade.direction == Direction.LONG:
                self.pos += trade.volume
            else:
                self.pos -= trade.volume

        def init_params(self, data):
            """"""
            # print("我在设置策略参数")
    return SmaStrategy("double_ma")

def save_data_json(data):
    result = {"result": data}

    class CJsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, obj)

    with open("data.json", "w") as f:
        json.dump(result, f, cls=CJsonEncoder)

def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("result")

def run_main(data):
    vessel = Vessel()
    vessel.add_data(data)
    stra = get_a_strategy()
    vessel.add_strategy(stra)
    vessel.set_params({"looper":
                           {"initial_capital": 100000,
                            "commission": 0.005,
                            "deal_pattern": "price",
                            "size_map": {"ag1912.SHFE": 15},
                            "today_commission": 0.005,
                            "yesterday_commission": 0.02,
                            "close_commission": 0.005,
                            "slippage_sell": 0,
                            "slippage_cover": 0,
                            "slippage_buy": 0,
                            "slippage_short": 0,
                            "close_pattern": "yesterday",
                            },
                       "strategy": {}
                       })
    vessel.run()
    from pprint import pprint
    result = vessel.get_result()
    pprint(result)


if __name__ == '__main__':
    data = load_data()
    for x in data:
        x['datetime'] = datetime.strptime(str(x['datetime']), "%Y-%m-%d %H:%M:%S")
    run_main(data)
```

例子二
```python
import json
from datetime import datetime, date
from ctpbee import LooperApi, Vessel
from ctpbee.constant import Direction
from indicator.interface import api

def get_data(start, end, symbol, exchange, level):
    """ using rqdatac to make an example """
    # import rqdatac as rq
    # from rqdatac import get_price, id_convert
    # username = "license"
    # password = "NK-Ci7vnLsRiPPWYwxvvPYdYM90vxN60qUB5tVac2mQuvZ8f9Mq8K_nnUqVspOpi4BLTkSLgq8OQFpOOj7L" \
    #            "t7AbdBZEBqRK74fIJH5vsaAfFQgl-tuB8l03axrW8cyN6-nBUho_6Y5VCRI63Mx_PN54nsQOpc1psIGEz" \
    #            "gND8c6Y=bqMVlABkpSlrDNk4DgG-1QXNknJtk0Kkw2axvFDa0E_XPMqOcBxifuRa_DFI2svseXU-8A" \
    #            "eLjchnTkeuvQkKh6nrfehVDiXjoMeq5sXgqpbgFAd4A5j2B1a0gpE3cb5kXb42n13fGwFaGris" \
    #            "8-eKzz_jncvuAamkJEQQV0aLdiw="
    # host = "rqdatad-pro.ricequant.com"
    # port = 16011
    # rq.init(username, password, (host, port))
    # symbol_rq = id_convert(symbol)
    # data = get_price(symbol_rq, start_date=start, end_date=end, frequency=level, fields=None,
    #                  adjust_type='pre', skip_suspended=False, market='cn', expect_df=False)
    # origin = data.to_dict(orient='records')
    # result = []
    # for x in origin:
    #     do = {}
    #     do['open_price'] = x['open']
    #     do['low_price'] = x['low']
    #     do['high_price'] = x['high']
    #     do['close_price'] = x['close']
    #     do['datetime'] = datetime.strptime(str(x['trading_date']), "%Y-%m-%d %H:%M:%S")
    #     do['symbol'] = symbol
    #     do['local_symbol'] = symbol + "." + exchange
    #     do['exchange'] = exchange
    #     result.append(do)
    # return result

def get_a_strategy():

    class SmaStrategy(LooperApi):

        def __init__(self, name):
            super().__init__(name)
            self.count = 1
            self.pos = 0
            self.bar_3 = api()  # 3分钟线
            
            self.allow_max_price = 5000  # 设置价格上限 当价格达到这个就卖出 防止突然跌
            self.allow_low_price = 4100  # 设置价格下限 当价格低出这里就卖 防止巨亏

            self.bar_3.open_json('indicator/json/zn1912.SHFE.json')

            # self.bar_3.open_csv('indicator/txt/orcl-2014.txt')

        def on_bar(self, bar):
            # todo: 简单移动平均线
            """ """
            self.bar_3.add_bar(bar)
            close = self.bar_3.close
            # 简单移动平均线
            sma = self.bar_3.sma()
            
            if self.allow_max_price <= close[-1] and self.pos > 0:
                self.action.sell(bar.close_price, self.pos, bar)

            if self.allow_low_price >= close[-1] and self.pos > 0:
                self.action.sell(bar.close_price, self.pos, bar)

            # 接连两天涨 买进
            if close[-1] > sma[-1] and close[-2] > sma[-2]:
                
                if self.pos == 0:
                    self.action.buy(bar.close_price, 1, bar)

                elif self.pos < 0:
                    self.action.cover(bar.close_price, 1, bar)
                    self.action.buy(bar.close_price, 1, bar)
            # 接连跌就卖
            if close[-1] < sma[-1] and close[-2] < sma[-2]:
                if self.pos == 0:
                    pass
                elif self.pos > 0:
                    self.action.sell(bar.close_price, 1, bar)
                    self.action.short(bar.close_price, 1, bar)

        def on_trade(self, trade):
            if trade.direction == Direction.LONG:
                self.pos += trade.volume
            else:
                self.pos -= trade.volume

        def init_params(self, data):
            """"""
            # print("我在设置策略参数")

    return SmaStrategy("double_ma")

def save_data_json(data):
    result = {"result": data}

    class CJsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, obj)

    with open("data.json", "w") as f:
        json.dump(result, f, cls=CJsonEncoder)

def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("result")

def run_main(data):
    vessel = Vessel()
    vessel.add_data(data)
    stra = get_a_strategy()
    vessel.add_strategy(stra)
    vessel.set_params({"looper":
                           {"initial_capital": 100000,
                            "commission": 0.005,
                            "deal_pattern": "price",
                            "size_map": {"ag1912.SHFE": 15},
                            "today_commission": 0.005,
                            "yesterday_commission": 0.02,
                            "close_commission": 0.005,
                            "slippage_sell": 0,
                            "slippage_cover": 0,
                            "slippage_buy": 0,
                            "slippage_short": 0,
                            "close_pattern": "yesterday",
                            },
                       "strategy": {}
                       })
    vessel.run()
    from pprint import pprint
    result = vessel.get_result()
    pprint(result)

if __name__ == '__main__':
    data = load_data()
    for x in data:
        x['datetime'] = datetime.strptime(str(x['datetime']), "%Y-%m-%d %H:%M:%S")
    run_main(data)
```

列子三
```python
import json
from datetime import datetime, date
from ctpbee import LooperApi, Vessel
from ctpbee.constant import Direction
from indicator.interface import api

def get_data(start, end, symbol, exchange, level):
    """ using rqdatac to make an example """
    # import rqdatac as rq
    # from rqdatac import get_price, id_convert
    # username = "license"
    # password = "NK-Ci7vnLsRiPPWYwxvvPYdYM90vxN60qUB5tVac2mQuvZ8f9Mq8K_nnUqVspOpi4BLTkSLgq8OQFpOOj7L" \
    #            "t7AbdBZEBqRK74fIJH5vsaAfFQgl-tuB8l03axrW8cyN6-nBUho_6Y5VCRI63Mx_PN54nsQOpc1psIGEz" \
    #            "gND8c6Y=bqMVlABkpSlrDNk4DgG-1QXNknJtk0Kkw2axvFDa0E_XPMqOcBxifuRa_DFI2svseXU-8A" \
    #            "eLjchnTkeuvQkKh6nrfehVDiXjoMeq5sXgqpbgFAd4A5j2B1a0gpE3cb5kXb42n13fGwFaGris" \
    #            "8-eKzz_jncvuAamkJEQQV0aLdiw="
    # host = "rqdatad-pro.ricequant.com"
    # port = 16011
    # rq.init(username, password, (host, port))
    # symbol_rq = id_convert(symbol)
    # data = get_price(symbol_rq, start_date=start, end_date=end, frequency=level, fields=None,
    #                  adjust_type='pre', skip_suspended=False, market='cn', expect_df=False)
    # origin = data.to_dict(orient='records')
    # result = []
    # for x in origin:
    #     do = {}
    #     do['open_price'] = x['open']
    #     do['low_price'] = x['low']
    #     do['high_price'] = x['high']
    #     do['close_price'] = x['close']
    #     do['datetime'] = datetime.strptime(str(x['trading_date']), "%Y-%m-%d %H:%M:%S")
    #     do['symbol'] = symbol
    #     do['local_symbol'] = symbol + "." + exchange
    #     do['exchange'] = exchange
    #     result.append(do)
    # return result

def get_a_strategy():

    class SmaStrategy(LooperApi):

        def __init__(self, name):
            super().__init__(name)
            self.count = 1
            self.pos = 0

            self.bar_3 = api()  # 3分钟线
            
            self.allow_max_price = 5000  # 设置价格上限 当价格达到这个就卖出 防止突然跌
            self.allow_low_price = 4100  # 设置价格下限 当价格低出这里就卖 防止巨亏

            self.bar_3.open_json('indicator/json/zn1912.SHFE.json')
      
            # self.bar_3.open_csv('indicator/txt/orcl-2014.txt')

        def on_bar(self, bar):
            # todo: 简单异同移动平均 macd
            """ """
            self.bar_3.add_bar(bar)
            close = self.bar_3.close
            # 简单异同移动平均 macd
            macd, signal, histo = self.bar_3.macd()
            
            if self.allow_max_price <= close[-1] and self.pos > 0:
                self.action.sell(bar.close_price, self.pos, bar)

            if self.allow_low_price >= close[-1] and self.pos > 0:
                self.action.sell(bar.close_price, self.pos, bar)

            if histo[-1] > 0:
                if self.pos == 0:
                    self.action.buy(bar.close_price, 1, bar)
            else:
                if self.pos > 0:
                    self.action.sell(bar.close_price, 1, bar)
                    self.action.short(bar.close_price, 1, bar)

        def on_trade(self, trade):
            if trade.direction == Direction.LONG:
                self.pos += trade.volume
            else:
                self.pos -= trade.volume

        def init_params(self, data):
            """"""
            # print("我在设置策略参数")

    return SmaStrategy("double_ma")

def save_data_json(data):
    result = {"result": data}

    class CJsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, obj)

    with open("data.json", "w") as f:
        json.dump(result, f, cls=CJsonEncoder)

def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("result")

def run_main(data):
    vessel = Vessel()
    vessel.add_data(data)
    stra = get_a_strategy()
    vessel.add_strategy(stra)
    vessel.set_params({"looper":
                           {"initial_capital": 100000,
                            "commission": 0.005,
                            "deal_pattern": "price",
                            "size_map": {"ag1912.SHFE": 15},
                            "today_commission": 0.005,
                            "yesterday_commission": 0.02,
                            "close_commission": 0.005,
                            "slippage_sell": 0,
                            "slippage_cover": 0,
                            "slippage_buy": 0,
                            "slippage_short": 0,
                            "close_pattern": "yesterday",
                            },
                       "strategy": {}
                       })
    vessel.run()
    from pprint import pprint
    result = vessel.get_result()
    pprint(result)

if __name__ == '__main__':
    data = load_data()
    for x in data:
        x['datetime'] = datetime.strptime(str(x['datetime']), "%Y-%m-%d %H:%M:%S")
    run_main(data)
```
