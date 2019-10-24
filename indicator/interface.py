from .plot import Cerebro


class Interface:

    def open_csv(self, file:str, start_time=None, end_time=None):
        Cerebro.open_csv(file, start_time, end_time)

    def open_json(self, file:str, start_time=None, end_time=None):
        Cerebro.open_json(file, start_time, end_time)

    def sma(self, n=15):
        data = Cerebro.ret_close
        return Cerebro.sma(data, n)

    def ema(self, n=12, alpha=None):
        data = Cerebro.ret_close
        return Cerebro.ema(data, n, alpha)

    def wma(self, n=30):
        data = Cerebro.ret_close
        return Cerebro.wma(data, n)

    def kd(self, n=14, f=3):
        data = Cerebro.ret_close
        return Cerebro.kd(data, n, f)

    def macd(self, n=12, m=20, f=9):
        data = Cerebro.ret_close
        return Cerebro.macd(data, n, m, f)

    def rsi(self, n=14, l=1):
        data = Cerebro.ret_close
        return Cerebro.rsi(data, n, l)

    def smma(self, n=10, alpha=15):
        data = Cerebro.ret_close
        return Cerebro.smma(data, n, alpha)

    def atr(self, n=14):
        data = Cerebro.ret_close
        return Cerebro.atr(data, n)

    def stdDev(self, n=20):
        data = Cerebro.ret_close
        return Cerebro.stdDev(data, n)

    def boll(self, n=20, m=2):
        data = Cerebro.ret_close
        return Cerebro.boll(data, n, m)

    def trix(self, n=15, m=1):
        data = Cerebro.ret_close
        return Cerebro.trix(data, n, m)

    def roc(self, n=12):
        data = Cerebro.ret_close
        return Cerebro.roc(data, n)

    def mtm(self, n=12):
        data = Cerebro.ret_close
        return Cerebro.mtm(data, n)

    def tema(self, n):
        data = Cerebro.ret_close
        return Cerebro.tema(data, n)

    def wr(self, n=14):
        data = Cerebro.ret_close
        return Cerebro.wr(data, n)

    def UltimateOscillator(self):
        pass

    def AroonIndicator(self):
        pass