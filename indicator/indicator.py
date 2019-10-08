from indicator.exprs import exprenv

class Indicator:
    def __init__(self):
        self._exprEnv = exprenv.ExprEnv()
        self._rid = 0
        self._params = []
        self._assigns = []
        self._outputs = []

    def addParameter(self, expr):
        self._params.append(expr)

    def addAssign(self, expr):
        self._assigns.append(expr)

    def addOutput(self, expr):
        self._outputs.append(expr)

    def getParamterCount(self):
        return len(self._params)

    def getParameterAt(self, index):
        return self._params[index]

    def getOutputCount(self):
        return len(self._outputs)

    def getOutputAt(self, index):
        return self._outputs[index]

    def clear(self):
        self._exprEnv.setFirstIndex(-1)
        cnt = len(self._assigns)
        for i in range(cnt):
            self._assigns[i].clear()
        cnt = len(self._outputs)
        for i in range(cnt):
            self._outputs.clear()

    def reserve(self, count):
        self._rid += 1
        cnt = len(self._assigns)
        for i in range(cnt):
            self._assigns[i].reserve(self._rid, count)
        cnt = len(self._outputs)
        for i in range(cnt):
            self._outputs[i].reserve(self._rid, count)

    def execute(self, ds, index):
        if index < 0:
            return
        self._exprEnv.setDataSource(ds)

        exprenv.ExprEnv.set(self._exprEnv)

        try:
            cnt = len(self._assigns)

            for i in range(cnt):
                self._assigns[i].assign(index)
            cnt = len(self._outputs)

            for i in range(cnt):
                self._outputs[i].assign(index)

            if self._exprEnv.getFirstIndex() < 0:
                self._exprEnv.setFirstIndex(index)

        except Exception as e:
            if self._exprEnv.getFirstIndex() >= 0:
                print(e)


    def getParameters(self):
        params = []
        cnt = len(self._params)
        for i in range(cnt):
            params.append(self._params[i].getValue())

        return params

    def setParameters(self, params):
        if isinstance(params, list) and len(params) == len(self._params):
            for i in self._params:
                self._params[i].setValue(params[i])


class MAIndicator(Indicator):
    def __init__(self):
        super().__init__()
        self.M1 = exprenv.ParameterExpr("M1", 2, 1000, 7)
        self.M2 = exprenv.ParameterExpr("M2", 2, 1000, 30)
        self.M3 = exprenv.ParameterExpr("M3", 2, 1000, 0)
        self.M4 = exprenv.ParameterExpr("M4", 2, 1000, 0)
        self.M5 = exprenv.ParameterExpr("M5", 2, 1000, 0)
        self.M6 = exprenv.ParameterExpr("M6", 2, 1000, 0)
        self.addParameter(self.M1)
        self.addParameter(self.M2)
        self.addParameter(self.M3)
        self.addParameter(self.M4)
        self.addParameter(self.M5)
        self.addParameter(self.M6)

    def getName(self):
        return "MA"


class EMAIndicator(Indicator):
    def __init__(self):
        super().__init__()
        self.M1 = exprenv.ParameterExpr("M1", 2, 1000, 7)
        self.M2 = exprenv.ParameterExpr("M2", 2, 1000, 30)
        self.M3 = exprenv.ParameterExpr("M3", 2, 1000, 0)
        self.M4 = exprenv.ParameterExpr("M4", 2, 1000, 0)
        self.M5 = exprenv.ParameterExpr("M5", 2, 1000, 0)
        self.M6 = exprenv.ParameterExpr("M6", 2, 1000, 0)
        self.addParameter(self.M1)
        self.addParameter(self.M2)
        self.addParameter(self.M3)
        self.addParameter(self.M4)
        self.addParameter(self.M5)
        self.addParameter(self.M6)

    def getName(self):
        return "EMA"


class VOLUMEIndicator(Indicator):
    def __init__(self):
        super().__init__()
        self.M1 = exprenv.ParameterExpr("M1", 2, 500, 5)
        self.M2 = exprenv.ParameterExpr("M2", 2, 500, 10)
        self.addParameter(self.M1)
        self.addParameter(self.M2)

    def getName(self):
        return "VOLUME"


class MACDIndicator(Indicator):
