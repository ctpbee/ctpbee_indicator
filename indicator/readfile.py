import os
import sys
import pandas as pd
import json
import time


class ReadFile:
    def __init__(self):
        self.count = int
        self.ret_data = None
        self.ret_low = None
        self.ret_high = None
        self.ret_date = None
        self.ret_close = None
        self.ret_volume = None

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, "_instance"):
    #         obj = super(ReadFile, cls)
    #         cls._instance = obj.__new__(cls, *args, **kwargs)
    #     return cls._instance

    def path(self, file):
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        # datapath = os.path.join(modpath, './datas/orcl-2014.txt')
        datapath = os.path.join(modpath, file)
        return datapath

    def dataColumns(self, data: str, startTime: str, endTime: str):
        self.ret_data = data  # data[startTime:endTime]
        self.count = len(self.ret_data)
        self.ret_date = self.ret_data.index
        self.ret_volume = self.ret_data['Volume']
        self.ret_low = self.ret_data['Low']
        self.ret_high = self.ret_data['High']
        self.ret_close = self.ret_data['Close']
        return self.ret_close

    def openCSV(self, file: str, startTime: str, endTime: str):
        """
        读取文件
        :param file: 文件名
        :param startTime: 开始读取时间
        :param endTime: 结束时间
        :return: dataframe对象
        """
        datapath = self.path(file)
        data = pd.read_csv(datapath, index_col=0, parse_dates=True)  # , index_col=0
        ret_close = self.dataColumns(self, data)  # , startTime, endTime
        return ret_close

    def openJSON(self, file: str, startTime: str, endTime: str):
        datapath = self.path(file)
        data_str = open(datapath).read()
        data_loads = json.loads(data_str)
        for data_lines in data_loads:
            for col in data_loads[data_lines]:
                time_local = time.localtime(float(col[0])/1000)
                col[0] = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        data = pd.DataFrame(data_loads.values(), columns=["Date", "Open", "High", "Low", "Close", "Volume"], index=0)
        ret_close = self.dataColumns(self, data, startTime, endTime)
        print(ret_close)
        return ret_close

File = ReadFile

ReadFile().openJSON("./ctpbee_desktop/ag1911.SHFE.json", '', '')
