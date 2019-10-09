import math

class ExprEnv:

    def get(self):
        return self.inst

    def set(self, env):
        self.inst = env

    def getDataSource(self):
        return self._ds

    def setDataSource(self, ds):
        self._ds = ds
        return self._ds

    def getFirstIndex(self):
        return self._firstIndex

    def setFirstIndex(self, n):
        self._firstIndex = n
        return self._firstIndex


ExprEnv.inst = None
ExprEnv._ds = None
ExprEnv._firstIndex = None


class Expr:
    def __init__(self):
        self._rid = 0

    def execute(self, index):
        pass

    def reserve(self, rid, count):
        pass

    def clear(self):
        pass

    @property
    def rid(self):
        return self._rid


class OpenExpr(Expr):
    def execute(self, index):
        return ExprEnv.get._ds[index].open


class HighExpr(Expr):
    def execute(self, index):
        return ExprEnv.get()._ds[index].high


class LowExpr(Expr):
    def execute(self, index):
        return ExprEnv.get()._ds[index].low


class CloseExpr(Expr):
    def execute(self, index):
        return ExprEnv.get()._ds[index].volume


class VolumeExpr(Expr):
    def execute(self, index):
        return ExprEnv.get()._ds[index].volume


class ConstExpr(Expr):
    def __init__(self, v):
        super().__init__()
        self._value = v

    def execute(self, index):
        return self._value


class ParameterExpr(Expr):
    def __init__(self, name, minValue, maxValue, defaultValue):
        super().__init__()
        self._name = name
        self._minValue = minValue
        self._maxValue = maxValue

        self._value = defaultValue

    def execute(self, index):
        return self._value

    def getMinValue(self):
        return self._minValue

    def getMaxValue(self):
        return self._maxValue

    def getDefaultValue(self):
        return self._value

    def getValue(self):
        return self._value


class OpAExpr(Expr):
    def __init__(self, a):
        super().__init__()
        self._exprA = a

    def reserve(self, rid, count):
        if self._rid < rid:
            self._rid = rid

            self._exprA.reserve(rid, count)

    def clear(self):
        self._exprA.clear()


class OpABExpr(Expr):
    def __init__(self, a, b):
        super().__init__()
        self._exprA = a
        self._exprB = b

    def reserve(self, rid, count):
        if self._rid < rid:
            self._rid = rid
            self._exprA.reserve(rid, count)
            self._exprB.reserve(rid, count)

    def clear(self):
        self._exprA.clear()
        self._exprB.clear()


class OpABCExpr(Expr):
    def __init__(self, a, b, c):
        super().__init__()
        self._exprA = a
        self._exprB = b
        self._exprC = c

    def reserve(self, rid, count):
        if self._rid < rid:
            self._rid = rid
            self._exprA.reserve(rid, count)
            self._exprB.reserve(rid, count)
            self._exprC.reserve(rid, count)

    def clear(self):
        self._exprA.clear()
        self._exprB.clear()
        self._exprC.clear()


class OpABCDExpr(Expr):
    def __init__(self, a, b, c, d):
        super().__init__()
        self._exprA = a
        self._exprB = b
        self._exprC = c
        self._exprD = d

    def execute(self, index):
        return -(self._exprA.execute(index))


class NegExpr(OpAExpr):
    def __init__(self, a):
        super().__init__(a)

    def execute(self, index):
        return -(self._exprA.execute(index))


class AddExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):
        return self._exprA.execute(index) + self._exprB.execute(index)


class SubExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):
        return self._exprA.execute(index) - self._exprB.execute(index)


class MulExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):
        a = self._exprA.execute(index)
        b = self._exprB.execute(index)
        if a == 0:
            return a
        if b == 0:
            # return (a > 0) ? 1000000: -1000000
            if a > 0:
                return 1000000
            else:
                return -1000000
        return a / b


class GtExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):

        if self._exprA.execute(index) > self._exprB.execute(index):
            return 1
        else:
            return 0


class LtExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):

        if self._exprA.execute(index) < self._exprB.execute(index):
            return 1
        else:
            return 0


class LeExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):

        if self._exprA.execute(index) <= self._exprB.execute(index):
            return 1
        else:
            return 0


class EqExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):

        if self._exprA.execute(index) == self._exprB.execute(index):
            return 1
        else:
            return 0


class MaxExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):
        return max(self._exprA.execute(index) < self._exprB.execute(index))


class AbsExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):
        return abs(self._exprA.execute(index))


class RefExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):
        pass


class AndExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):
        if self._exprA.execute(index) != 0 and self._exprB.execute(index) != 0:
            return 1
        else:
            return 0


class OrExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def execute(self, index):
        if self._exprA.execute(index) != 0 or self._exprB.execute(index) != 0:
            return 1
        else:
            return 0


class IfExpr(OpABCExpr):
    def __init__(self, a, b, c):
        super().__init__(a, b, c)

    def execute(self, index):
        if self._exprA.execute(index) != 0:
            return self._exprB.execute(index)
        return self._exprC.execute(index)


class AssignExpr(OpAExpr):
    def __init__(self, name, a):
        super().__init__(a)
        self._name = name
        self._buf = []

    def getName(self):
        return self._name

    def execute(self, index):
        return self._buf[index]

    def assign(self, index):
        self._buf[index] = self._exprA.execute(index)
        pass

    def reserve(self, rid, count):
        if self._rid < rid:
            for c in range(count, 0, -1):
                self._buf.append('NaN')
        super().reserve(rid, count)

    def clear(self):
        super().clear()
        self._buf = []


class OutputExpr(AssignExpr):
    def __init__(self, name, a, style, color):
        super().__init__(name, a)

    def getStyle(self):
        pass

    def getColor(self):
        pass


class RangeExpr(OpABExpr):
    def __init__(self, a, b):
        super().__init__(a, b)
        self._range = -1
        self._buf = []

    def getRange(self):
        return self._range

    def initRange(self):
        self._range = self._exprB.execute(0)
        return self._range

    def execute(self, index):
        if self._range < 0:
            self.initRange()
        rA = self._buf[index].resultA = self._exprA.execute(index)
        self._buf[index].result = self.calcResult(index, rA)
        return self._buf[index].result

    def reserve(self, rid, count):
        if self._rid < rid:
            for i in range(count, 0, -1):
                self._buf.append({"resultA": "NaN", "result": "NaN"})
        super().reserve(rid, count)

    def clear(self):
        super().clear()
        self._range = -1
        self._buf = []


class HhvExpr(RangeExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def calcResult(self, index, resultA):
        if self._range == 0:
            return "NaN"
        first = ExprEnv.get()._firstIndex
        if first < 0:
            return resultA
        if index > first:
            n = self._range
            result = resultA
            start = index - n + 1
            i = max(first, start)
            for i in range(i, index):
                p = self._buf[i]
                if result < p.resultA:
                    result = p.resultA
                return result
        else:
            return resultA


class LlvExpr(RangeExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def calcResult(self, index, resultA):
        if self._range == 0:
            return "NaN"
        first = ExprEnv.get()._firstIndex
        if first < 0:
            return resultA
        if index > first:
            n = self._range
            result = resultA
            start = index - n + 1
            i = max(first, start)
            for i in range(i, index):
                p = self._buf[i]
                if result > p.resultA:
                    result = p.resultA
                return result
        else:
            return resultA


class CountExpr(RangeExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def calcResult(self, index, resultA):
        if self._range == 0:
            return "NaN"
        first = ExprEnv.get()._firstIndex
        if first < 0:
            return resultA
        if index >= first:
            n = self._range - 1
            if n > index - first:
                n = index - first
            count = 0
            for c in range(n, 0, -1):
                if self._buf[index-c].resultA != 0.0:
                    count += 1
            return count
        else:
            return 0


class SumExpr(RangeExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def calcResult(self, index, resultA):
        first = ExprEnv.get()._firstIndex
        if first < 0:
            return resultA
        if index > first:
            n = self._range
            if n == 0 and n >= index + 1 - first:
                return self._buf[index-1].result+resultA
            return self._buf[index - 1].resultA - self._buf[index - n].resultA
        else:
            return resultA


class StdExpr(RangeExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def calcResult(self, index, resultA):
        if self._range == 0:
            return None
        stdData = self._stdBuf[index]
        first = ExprEnv.get()._firstIndex
        if first < 0:
            stdData.resultMA = resultA
            return 0.0
        if index > first:
            n = self._range
            if n >= index + 1 - first:
                n = index + 1 - first
                stdData.resultMA = self._stdBuf[index - 1].resultMA * (1.0 - 1.0 / n) + (resultA / n)
            else:
                stdData.resultMA = self._stdBuf[index - 1].resultMA + (resultA - self._buf[index - n].resultA) / n
            sum = 0
            for i in range(index-n+1, index):
            # for (i = index - n + 1; i <= index; i++)
                sum += pow(self._buf[i].resultA - stdData.resultMA, 2)

            return math.sqrt(sum / n)
        stdData.resultMA = resultA
        return 0.0

    def reserve(self, rid, count):
        if self._rid < rid:
            for c in range(count, 0):
                self._stdBuf.append({"resultMA": "NaN"})
        super().reserve(rid, count)

    def clear(self):
        super().clear()
        self._stdBuf = []


class MaExpr(RangeExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def calsResult(self, index, resultA):
        if self._range == 0:
            return "NaN"
        first = ExprEnv.get()._firstIndex
        if first < 0:
            return resultA
        if index > first:
            n = self._range
            if n >= index + 1 - first:
                n = index + 1 - first
                return self._buf[index-1].result*(1.0-1.0/n)+(resultA/n)
            return self._buf[index-1].result+(resultA-self._buf[index-n].resultA)/n
        else:
            return resultA


class EmaExpr(RangeExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def initRange(self):
        super().initRange()
        self._alpha = 2.0 / (self._range + 1)

    def calsResult(self, index, resultA):
        if self._range == 0:
            return "NaN"
        first = ExprEnv.get()._firstIndex
        if first < 0:
            return resultA
        if index > first:
            prev = self._buf[index-1]
            return self._alpha * (resultA - prev.result) + prev.result
        return resultA


class ExpmemaExpr(EmaExpr):
    def __init__(self, a, b):
        super().__init__(a, b)

    def calsResult(self, index, resultA):
        first = ExprEnv.get()._firstIndex
        if first < 0:
            return resultA
        if index > first:
            n = self._range
            prev = self._buf[index - 1]
            if n >= index + 1 -first:
                n = index + 1 -first
                return prev.result*(1.0-1.0/n)+(resultA/n)
            return self._alpha * (resultA - prev.result) + prev.result
        return resultA


class SmaExpr(RangeExpr):
    def __init__(self, a, b, c):
        super().__init__(a, b)
        self._exprC = c
        self._mul = None

    def initRange(self):
        super().initRange()
        self._mul = self._exprC.execute(0)

    def calsResult(self, index, resultA):
        if self._range == 0:
            return "NaN"
        first = ExprEnv.get()._firstIndex
        if first < 0:
            return resultA
        if index > first:
            n = self._range
            prev = self._buf[index - 1]
            if n >= index + 1 -first:
                n = index + 1 -first
            return ((n-1)*self._buf[index-1].result+resultA*self._mul)/n
        return resultA


class SarExpr(OpABCDExpr):
    def __init__(self, a, b, c, d):
        super().__init__(a, b, c, d)
        self._buf = []
        self._range = -1
        self._min = None
        self._step = None
        self._max = None

    def execute(self, index):
        if self._range < 0:
            self._range = self._exprA.execute(0)
            self._min = self._exprB.execute(0) / 100.0
            self._step = self._exprC.execute(0) / 100.0
            self._max = self._exprD.execute(0) / 100.0
        data = self._buf[index]
        exprEnv = ExprEnv.get()
        first = exprEnv._firstIndex
        if first < 0:
            data.longPos = True
            data.sar = exprEnv._ds.getDataAt(index).low
            data.ep = exprEnv._ds.getDataAt(index).high
            data.af = 0.02
        else:
            high = exprEnv._ds.getDataAt(index).high
            low = exprEnv._ds.getDataAt(index).low
            prev = self._buf[index - 1]
            data.sar = prev.sar + prev.af * (prev.ep - prev.sar)
            if prev.longPos:
                data.longPos = True
                if high > prev.ep:
                    data.ep = high
                    data.af = min(prev.af + self._step, self._max)
                else:
                    data.ep = prev.ep
                    data.af = prev.af
                if data.sar > low:
                    data.longPos = False
                    i = index - self._range + 1
                    for i in range(max(i, first), index):
                        h = exprEnv._ds.getDataAt(i).high
                        if high < h:
                            high = h
                    data.sar = high
                    data.ep = low
                    data.af = 0.02
            data.longPos = False
            if low < prev.ep:
                data.ep = low
                data.af = min(prev.af + self._step, self._max)
            else:
                data.ep = prev.ep
                data.af = prev.af
            if data.sar<high:
                data.longPos = True
                i = index - self._range + 1
                for i in range(max(i, first), index):
                    l = exprEnv._ds.getDataAt(i).low
                    if low > l: low = l
                data.sar = low
                data.ep = high
                data.af = 0.02
        return data.sar
    def reserve(self, rid, count):
        if self._rid < rid:
            for c in range(count, 0, -1):
                # (let c = count; c > 0; c--)
                self._buf.append({"longPos":True, "sar": "NaN", "ep": "NaN", "af": "NaN"});
        super().reserve(rid, count)

    def clear(self):
        super().clear()
        self._range = -1