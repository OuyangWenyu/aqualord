# -*- coding: utf-8 -*-
"""
从FY-4A标称数据提取指定范围指定通道
Created on 2018/11/14 12:46:47
@author: modabao
"""

from h5py import File as h5File
import numpy as np
from projection import latlon2lc


# 各分辨率文件包含的通道号
CONTENTS = {"0500M": ("Channel02",),
            "1000M": ("Channel01", "Channel02", "Channel03"),
            "2000M": tuple([f"Channel{x:02d}" for x in range(1, 8)]),
            "4000M": tuple([f"Channel{x:02d}" for x in range(1, 15)])}
# 各分辨率行列数
SIZES = {"0500M": 21984,
         "1000M": 10992,
         "2000M": 5496,
         "4000M": 2748}


class FY4A_H5(object):
    """
    """
    def __init__(self, h5name, channelnames=None):
        """
        获得h5文件对象、记录读取状态
        """
        self.h5file = h5File(h5name, 'r')
        self.channelnames = channelnames or CONTENTS[h5name[-15:-10]]
        self.channels = {x: None for x in self.channelnames}
        self.geo_range = None
        self.l = None
        self.c = None
        self.l_begin = self.h5file.attrs["Begin Line Number"]
        self.l_end = self.h5file.attrs["End Line Number"]
        # if geo_range is not None:
        #     self.lat_S, self.lat_N, self.lon_W, self.lon_E, self.step = geo_range

    def __del__(self):
        """
        确保关闭h5文件
        """
        self.h5file.close()

    def extract(self, channelname, geo_range=None):
        """
        最邻近插值提取
        l：行号
        c：列号
        channelnames：提取的通道名（两位数字字符串序列）
        返回字典
        暂时没有处理缺测值（异常）
        REGC超出范围未解决
        """
        NOMChannelname = "NOM" + channelname
        CALChannelname = "CAL" + channelname
        # 若geo_range没有指定，则读取全部数据，不定标
        if geo_range is None:
            channel = self.h5file[NOMChannelname][()]
            self.channels[channelname] = channel
            return None
        geo_range = eval(geo_range)
        if self.geo_range != geo_range:
            self.geo_range = geo_range
            lat_S, lat_N, lon_W, lon_E, step = geo_range
            lat = np.arange(lat_N, lat_S-0.005, -step) 
            lon = np.arange(lon_W, lon_E+0.005, step)
            lon, lat = np.meshgrid(lon, lat)
            self.l, self.c = latlon2lc(lat, lon, "4000M")  # 求标称全圆盘行列号
            self.l = np.rint(self.l).astype(np.uint16)
            self.c = np.rint(self.c).astype(np.uint16)
        # DISK全圆盘数据和REGC中国区域数据区别在起始行号和终止行号
        channel = self.h5file[NOMChannelname][()][self.l - self.l_begin, self.c]
        CALChannel = self.h5file[CALChannelname][()]  # 定标表
        self.channels[channelname] = CALChannel[channel]  # 缺测值！？



# 演示导出指定范围数据到一个.nc文件
if __name__ == "__main__":
    from os import listdir
    from os.path import join
    from datetime import datetime
    from netCDF4 import date2num, Dataset as ncDataset
    from matplotlib import pyplot as plt
    h5path = r"..\data"  # FY-4A一级数据所在路径
    ncname = r"..\data\test.nc"
    h5list = [join(h5path, x) for x in listdir(h5path)
              if "4000M" in x and "FDI" in x]
    geo_range = "10, 54, 70, 140, 0.05"
    lat_S, lat_N, lon_W, lon_E, step = eval(geo_range)
    lat = np.arange(lat_N, lat_S-0.01, -step) 
    lon = np.arange(lon_W, lon_E+0.01, step)
    channelnames = ("Channel12",)  # 测试数据Channel02有问题
    # 创建nc文件
    ncfile = ncDataset(ncname, 'w', format="NETCDF4")
    ncfile.createDimension("lat", len(lat))
    ncfile.createDimension("lon", len(lon))
    ncfile.createDimension("time")  # 不限长
    nclat = ncfile.createVariable("lat", "f4", ("lat",))
    nclon = ncfile.createVariable("lon", "f4", ("lon",))
    nctime = ncfile.createVariable("time", "f8", ("time",))
    nctime.units = "minutes since 0001-01-01 00:00:00.0"
    t = 0
    for channelname in channelnames:
        ncfile.createVariable(channelname, "f4", ("time", "lat", "lon"))
    ncfile.set_auto_mask(False)
    # 向nc文件中写入
    nclat[:] = lat
    nclon[:] = lon
    lon, lat = np.meshgrid(lon, lat)
    for h5name in h5list:
        fy4a_h5 = FY4A_H5(h5name, channelnames)
        print("FY4A_H5实例化成功")
        for channelname in channelnames:
            fy4a_h5.extract(channelname, geo_range)
            ncfile[channelname][t, :, :] = fy4a_h5.channels[channelname]
            print(channelname + "读取成功")
        time = datetime.strptime(h5name[-45: -33], "%Y%m%d%H%M%S")
        nctime[t] = date2num(time, nctime.units)
        ncfile.sync()  # 手动写入硬盘
        t += 1
        plt.figure(h5name[-45: -31])
        plt.imshow(fy4a_h5.channels["Channel12"], cmap="gray_r")
        plt.show()
    ncfile.close()
