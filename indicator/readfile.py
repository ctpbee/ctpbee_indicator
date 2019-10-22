import os
import sys
import csv
import json
import time
import pandas as pd
from datetime import datetime, date


class ReadFile:
    def __init__(self):
        self.count = int                    # 数量
        self.ret_data = None                # 总数据
        self.ret_low = None                 # 最低价
        self.ret_high = None                # 最高价
        self.ret_date = None                # 时间
        self.ret_close = None               # 收盘价
        self.ret_volume = None              # 成交量
        self.open_file_name = None          # 文件名
        self.open_file_start = None         # 开始时间

    def update_bar(self, datas, opens=True):
        """
        :param data: 数据类型
                        [time, open, high, low, close, volume]
                        [1883823344, 22, 44, 55, 55, 6666]
        :param opens: 开关
        :return:
        """
        if not datas:
            assert "type error or type is None"
        data = [datas["datetime"], datas["open_price"], datas["high_price"], datas["low_price"], datas["close_price"],
                554]

        if isinstance(data[0], datetime):
            data[0] = data[0].strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(data[0], date):
            data[0] = data[0].strftime('%Y-%m-%d')
        else:
            time_local = time.localtime(float(data[0]) / 1000)
            data[0] = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        if opens:
            if self.open_file_name.endswith(".csv"):
                with open(self.open_file_name, 'a+', newline='') as f:
                    w_data = csv.writer(f)
                    w_data.writerows(data)
            if self.open_file_name.endswith(".json"):
                with open(self.open_file_name, 'r') as jr:
                    r_json = json.loads(jr.read())
                    r_name = [name for name in r_json][0]
                    r_json[r_name].append(data)
                with open(self.open_file_name, 'w') as jw:

                    json.dump(r_json, jw)

            if self.open_file_name.endswith(".txt"):
                with open(self.open_file_name, 'a+') as t:
                    txt = "\n" + str(data).strip("[]")
                    t.write(txt)

        else:
            self.count += 1
            self.ret_data.loc[data[0]] = data[1:]
            self.ret_close = self.ret_data["Close"]
            self.ret_high = self.ret_data["High"]
            self.ret_low = self.ret_data["Low"]
            self.ret_date = self.ret_data["Date"]
            self.ret_volume = self.ret_data["Volume"]

    def save_file(self, data):
        """保存数据"""
        pass

    def path(self, file):
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        datapath = os.path.join(modpath, file)
        self.open_file_name = datapath
        return datapath

    def data_columns(self, data: str, start_time: str, end_time=None):
        self.open_file_start = start_time
        if end_time:
            self.ret_data = data[start_time:end_time]
        else:
            self.ret_data = data

        self.ret_date = self.ret_data.index
        self.count = len(self.ret_data)
        self.ret_volume = self.ret_data['Volume']
        self.ret_low = self.ret_data['Low']
        self.ret_high = self.ret_data['High']
        self.ret_close = self.ret_data['Close']
        return self.ret_close

    def open_csv(self, file: str, start_time: str, end_time=None):
        """
        读取文件
        :param file: 文件名
        :param start_time: 开始读取时间
        :param end_time: 结束时间
        :return: dataframe对象
        """
        datapath = self.path(file)
        data = pd.read_csv(datapath, index_col=0, parse_dates=True)  # , index_col=0
        ret_close = self.data_columns(data, start_time, end_time)
        return ret_close

    def open_json(self, file: str, start_time: str, end_time=None):
        datapath = self.path(file)
        data_str = open(datapath).read()
        data_loads = json.loads(data_str)
        for data_name, data_all in data_loads.items():
            data_lines = data_all
            # for col in data_lines:
            #     time_local = time.localtime(float(col[0])/1000)
            #     col[0] = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        data = pd.DataFrame(data_lines)
        data.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        data.set_index(["Date"], inplace=True)
        ret_close = self.data_columns(data, start_time, end_time)
        return ret_close


File = ReadFile
