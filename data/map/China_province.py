# -*- coding: utf-8 -*-
"""
中国省级行政区划China_province
Created on 2018/10/24 10:43:02
@author: modabao
"""

import cartopy.io.shapereader as shpreader


def __extract():
    """
    读取中国省级行政区划.shp文件
    provinces_geometrys：geometry列表
    provinces_attributes：attribute列表
    """
    shpname = r"China_province"
    provinces_records = list(shpreader.Reader(shpname).records())
    provinces_geometrys = [x.geometry for x in provinces_records]
    provinces_attributes = [x.attributes for x in provinces_records]
    return provinces_geometrys, provinces_attributes


provinces_geometrys, provinces_attributes = __extract()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    PlateCarree = ccrs.PlateCarree()
    plt.figure("Demo")
    ax = plt.axes(projection=PlateCarree)
    ax.add_geometries(provinces_geometrys, PlateCarree,
                      edgecolor='black', facecolor='None')
    ax.set_xlim((70, 140))
    ax.set_ylim((0, 60))
    ax.set_xticks([80, 100, 120, 140], PlateCarree)
    ax.set_yticks([0, 20, 40, 60], PlateCarree)
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    plt.show()