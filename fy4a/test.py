# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from extract import extract
from projection import latlon2lc, lc2latlon
from China_map import provinces_geometrys

h5name = (r".\testdata\FY4A-_AGRI--_N_REGC_1047E_L1-_FDI-_MULT_NOM_"
          "20180726051500_20180726051916_4000M_V0001.HDF")
step = 0.05
lat_low, lat_high = 10, 54
lon_left, lon_right = 70, 140
# 开始经纬度转行列号（内存充足情况下）
lat0 = int(1000 * lat_low)
lat1 = int(1000 * lat_high)
lon0 = int(1000 * lon_left)
lon1 = int(1000 * lon_right)
step_ = int(step * 1000)
lat = np.arange(lat1, lat0-1, -step_) / 1000  # 40~20°N
lon = np.arange(lon0, lon1+1, step_) / 1000  # 110~130°E
lon, lat = np.meshgrid(lon, lat)  # 构造经纬度网格
l, c = latlon2lc(lat, lon, "4000M")
channels = extract(h5name, l, c, channelnums=["12"])
channel12 = channels["Channel12"]

PlateCarree = ccrs.PlateCarree()
plt.figure("Tbb云顶亮温（Channel12）")
ax = plt.axes(projection=PlateCarree)
ax.add_geometries(provinces_geometrys, PlateCarree,
                  edgecolor='black', facecolor='None')
extent=[lon_left - 0.025, lon_right + 0.025, lat_low - 0.025, lat_high + 0.025]
ax.imshow(channel12, cmap="gray", transform=PlateCarree, origin='upper',
          extent=extent)
ax.set_xticks(list(range(lon_left, lon_right+1, 10)), PlateCarree)
ax.set_yticks(list(range(lat_low, lat_high+1, 10)), PlateCarree)
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
ax.coastlines()
plt.show()
plt.savefig(r".\testdata\Tbb云顶亮温（Channel12）")



channels = extract(h5name, channelnums=["12"])
begin = []
end = []
channel12 = channels["Channel12"]
for l, line in enumerate(channel12):
    for c, pixel in enumerate(line):
        if pixel < 65534:
            begin.append((l, c))
            for c1, pixel1 in enumerate(line[c:]):
                if pixel1 >= 65534:
                    end.append((l, c+c1-1))
                    break
            break
southline = [(begin[-1][0], x) for x in range(begin[-1][1], end[-1][1]+1)]
northline = [(begin[0][0], x) for x in range(begin[0][1], end[0][1]+1)]
temp = begin + southline + end[::-1] + northline[::-1]
temp = np.array(temp)
l = temp[:, 0] + 183
c = temp[:, 1]
lat, lon = lc2latlon(l, c, "4000M")
plt.figure("REGC大致范围")
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=100))
ax.plot(lon, lat, "b-", transform=PlateCarree)
ax.add_geometries(provinces_geometrys, PlateCarree,
                  edgecolor='black', facecolor='None')
ax.set_xticks(list(range(20, 180+1, 20)), PlateCarree)
ax.set_yticks(list(range(0, 70+1, 10)), PlateCarree)
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
ax.coastlines()
ax.set_xlim((-80, 90))
plt.show()
plt.savefig(r".\testdata\REGC大致范围")

