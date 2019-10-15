import os
import sys
import pandas as pd


class ReadFile:
    def __init__(self):
        self.count = int
        self.ret_data = None
        self.ret_low = None
        self.ret_high = None
        self.ret_date = None
        self.ret_close = None
        self.ret_volume = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            obj = super(ReadFile, cls)
            cls._instance = obj.__new__(cls, *args, **kwargs)
        return cls._instance

    def open(self, file: str, startTime: str, endTime: str):
        """
        读取文件
        :param file: 文件名
        :param startTime: 开始读取时间
        :param endTime: 结束时间
        :return: dataframe对象
        """
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        # datapath = os.path.join(modpath, './datas/orcl-2014.txt')
        datapath = os.path.join(modpath, file)
        data = pd.read_csv(datapath, index_col=0, parse_dates=True)  # , index_col=0
        print(data, type(data))
        self.ret_data = data[startTime:endTime]
        self.count = len(self.ret_data)
        self.ret_date = self.ret_data.index
        self.ret_volume = self.ret_data['Volume']
        self.ret_low = self.ret_data['Low']
        self.ret_high = self.ret_data['High']
        self.ret_close = self.ret_data['Close']
        return self.ret_close


File = ReadFile