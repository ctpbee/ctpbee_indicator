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
        return ExprEnv.get()._ds.getDataAt(index).open


class HighExpr(Expr):
    def execute(self, index):
        return ExprEnv.get()._ds.getDataAt(index).high


class LowExpr(Expr):
    def execute(self, index):
        return ExprEnv.get()._ds.getDataAt(index).low


class CloseExpr(Expr):
    def execute(self, index):
        return ExprEnv.get()._ds.getDataAt(index).volume


class VolumeExpr(Expr):
    def execute(self, index):
        return ExprEnv.get()._ds.getDataAt(index).volume


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
