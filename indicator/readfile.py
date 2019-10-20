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

    def newBar(self, data):
        """数据类型
            [time, open, high, low, close, volume]
        """
        self.count += 1
        self.ret_data.append(data)
        self.ret_close = self.ret_close.tolist().append(data[4])
        self.ret_high = self.ret_high.tolist().append(data[2])
        self.ret_low = self.ret_low.tolist().append(data[3])
        self.ret_date = self.ret_date.tolist().append(data[0])
        self.ret_volume = self.ret_volume.tolist().append(data[5])

    def path(self, file):
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        # datapath = os.path.join(modpath, './datas/orcl-2014.txt')
        datapath = os.path.join(modpath, file)
        return datapath

    def dataColumns(self, data: str, startTime: str, endTime=None):
        if endTime:
            self.ret_data = data[startTime:endTime]
        else:
            self.ret_data = data
        self.ret_date = self.ret_data.index
        self.count = len(self.ret_data)
        self.ret_volume = self.ret_data['Volume']
        self.ret_low = self.ret_data['Low']
        self.ret_high = self.ret_data['High']
        self.ret_close = self.ret_data['Close']
        return self.ret_close

    def openCSV(self, file: str, startTime: str, endTime=None):
        """
        读取文件
        :param file: 文件名
        :param startTime: 开始读取时间
        :param endTime: 结束时间
        :return: dataframe对象
        """
        datapath = self.path(file)
        data = pd.read_csv(datapath, index_col=0, parse_dates=True)  # , index_col=0
        ret_close = self.dataColumns(data, startTime, endTime)
        return ret_close

    def openJSON(self, file: str, startTime: str, endTime=None):
        datapath = self.path(file)
        data_str = open(datapath).read()
        data_loads = json.loads(data_str)
        for data_name, data_all in data_loads.items():
            data_lines = data_all
            for col in data_lines:
                time_local = time.localtime(float(col[0])/1000)
                col[0] = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        data = pd.DataFrame(data_lines)
        data.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        data.set_index(["Date"], inplace=True)
        ret_close = self.dataColumns(data, startTime, endTime)
        return ret_close


File = ReadFile
