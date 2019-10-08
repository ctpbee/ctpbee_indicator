class DataSource:
    def __init__(self, name):
        self._name = name

    def getUpdateMode(self):
        return self._updateMode

    def getUpdateMode(self, mode):
        self._updateMode = mode

    def getCacheSize(self):
        return 0

    def getDataCount(self):
        return 0

    def getDataAt(self, index):
        return self._dataItems[index]


class MainDataSource:
    def __init__(self):
        self._erasedCount = 0
        self._dataItems = []
        self._decimalDigits = 0

    def getCacheSize(self):
        return len(self._dataItems)

    def getDataCount(self):
        return len(self._dataItems)

    def getUpdataCount(self):
        pass

    def getAppendedCount(self):
        pass

    def getErasedCount(self):
        pass

    def getDecimalDigits(self):
        pass

    def calcDecimalDigits(self, v):
        num = str(v)
        i = num.index('.')
        if i < 0:
            return 0
        return (len(num)-1)-i

    def getLastData(self):
        count = self.getDataCount()
        if count < 1:
            return -1
        return self.getDataAt(count-1)

    def getDataAt(self, index):
        return self._dataItems[index]

    def update(self, data):
        self._dataItems = []
        cnt = len(data)
        for i in range(cnt):
            e = data[i]
            for n in range(4):
                d = self.calcDecimalDigits(e[n])
                if self._decimalDigits < d:
                    self._decimalDigits = d
            self._dataItems.append({
                "date": e[0],
                "open": e[1],
                "high": e[2],
                "low": e[3],
                "close": e[4],
                "volume": e[5]
            })
        return True