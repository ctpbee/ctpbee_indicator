"""
    当前回测示例
    1.当前数据基于rq进行下载的
    2.首先你需要调用get_data 来获得rq的数据 ，然后save_to_json保存到 json文件中去，主要在此过程中你需要手动对数据加入symbol等
    3.然后通过load_data函数重复调用数据
    4.调用run_main进行回测
    当前的strategy是借助vnpy的 ArrayManager . 你需要对此实现一些额外的安装操作
    需要额外安装的包
    ta-lib,  rqdatac( 后面需要被取代  ？？ Maybe use quantdata )
    目前暂时不够完善   ---> hope it will be a  very fancy framework
    written by somewheve  2019-9-30 08:43
"""

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
            self.bar_5 = api()  # 5分钟bar线
            self.bar_3 = api()  # 3分钟bar线
            self.bar_3.open_json('indicator/json/zn1912.SHFE.json')  # 读取本地数据
            self.bar_5.open_json('indicator/json/zn1912.SHFE.json')

            self.allow_max_price = 5000  # 设置价格上限 当价格达到这个就卖出 防止突然跌
            self.allow_low_price = 2000  # 设置价格下限 当价格低出这里就卖 防止巨亏

            # self.bar_3.open_csv('indicator/txt/orcl-2014.txt')

        def on_bar(self, bar):
            # todo: 简单移动平均线
            """ """
            self.bar_3.add_bar(bar)
            close = self.bar_3.close
            # 简单移动平均线
            # sma = self.bar_3.sma()
            # 加权移动
            # wma = self.bar_3.wma()
            # k d
            # k, d = self.bar_3.kd()
            # std
            # std = self.bar_3.bar_3.stdDev()
            # boll
            # t, m, b = self.bar_3.boll()
            # roc
            # roc = self.bar_3.roc()
            # mtm
            # mtm = self.bar_3.mtm()
            # wr
            # wr = self.bar_3.wr()
            # macd
            macd = self.bar_3.macd()
            # rsi
            # rsi = self.bar_3.rsi()
            # atr
            # atr = self.bar_3.atr()
            # tema
            # tema = self.bar_3.tema()
            # ema
            # ema = self.bar_3.ema()
            # trix = self.bar_3.trix()
            # smma = self.bar_3.smma()

            if self.allow_max_price < close[-1] and self.pos > 0:
                self.action.sell(bar.close_price, self.pos, bar)

            if self.allow_low_price > close[-1] and self.pos > 0:
                self.action.sell(bar.close_price, self.pos, bar)

            if macd[-1] > 0:
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

    class MacdStrategy(LooperApi):
        # todo: 简单异同移动平均 macd
        boll_window = 18
        boll_dev = 3.4
        cci_window = 10
        atr_window = 30
        sl_multiplier = 5.2
        fixed_size = 1

        boll_up = 0
        boll_down = 0
        cci_value = 0
        atr_value = 0

        intra_trade_high = 0
        intra_trade_low = 0
        long_stop = 0
        short_stop = 0

        parameters = ["boll_window", "boll_dev", "cci_window",
                      "atr_window", "sl_multiplier", "fixed_size"]
        variables = ["boll_up", "boll_down", "cci_value", "atr_value",
                     "intra_trade_high", "intra_trade_low", "long_stop", "short_stop"]

        def __init__(self, name):
            super().__init__(name)
            self.pos = 0

        def on_bar(self, bar):
            api.open_csv('indicator/txt/orcl-2014.txt')
            api.add_bar(bar, opens=True)
            close = api.close
            macd = api.macd()
            # 如果当前macd大于0就买
            if macd[-1] > 0:
                if self.pos == 0:
                    pass
                elif self.pos > 0:
                    self.action.cover(bar.close_price, 1, bar)
                    self.action.buy(bar.close_price, 1, bar)
            # 如果小于就卖
            else:
                if self.pos > 0:
                    self.action.sell(bar.close_price, 1, bar)
                    self.action.short(bar.close_price, 1, bar)

        def on_trade(self, trade):
            if trade.direction == Direction.LONG:
                self.pos += trade.volume
            else:
                self.pos -= trade.volume

        def on_order(self, order):
            pass

    return SmaStrategy("double_ma")
    # return MacdStrategy("double_ma")


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
    # data = get_data(start="2019-1-5", end="2019-9-1", symbol="ag1912", exchange="SHFE", level="15m")
    # save_data_json(data)

    data = load_data()
    for x in data:
        x['datetime'] = datetime.strptime(str(x['datetime']), "%Y-%m-%d %H:%M:%S")
    run_main(data)

