# coding: utf-8
"""
读取中国自动站与CMORPH降水产品融合的逐时降水量网格数据集（1.0版）数据

Created on 2019/03/13 10:29
@author: modabao
"""


import numpy as np


def read(filename):
    """
    Args:
        filename: 文件名
        
    Returns:
        crain: 降水量mm <numpy.ndarray>
        gsamp: 雨量计数量 <numpy.ndarray>
    """
    data = np.fromfile(filename, dtype="<f4")
    data = data.reshape((880, 700), order='C')[::-1]
    gsamp = data[:440]
    crain = data[440:]
    return crain, gsamp


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.transforms as mtransforms
    import matplotlib as mpl
    import cartopy.crs as ccrs
    import cartopy.io.shapereader as shpreader
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    from matplotlib.font_manager import FontProperties
    
    filename = (r"..\data\surf_cli_chn_merge_cmp_pre_hour_grid_0.10"
                r"\surf_cli_chn_merge_cmp_pre_hour_grid_0.10"
                r"surf_cli_chn_merge_cmp_pre_hour_grid_0.10-2018081707.grd")
    crain, gsamp = read(filename)
    crain[crain==-999] = np.nan
    
    shpname = r"..\data\map\China_province"
    provinces_records = list(shpreader.Reader(shpname).records())
    provinces_geometrys = [x.geometry for x in provinces_records]

    font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc")
    PlateCarree = ccrs.PlateCarree()
    fig = plt.figure("Demo", figsize=(9, 6), dpi=100, constrained_layout=True )
    ax = plt.axes(projection=PlateCarree)
    ax.add_geometries(provinces_geometrys, PlateCarree,
                      edgecolor="gray", facecolor='None')
    extent=[70.05, 139.95, 15.05, 59.95]
    cmap = mpl.colors.ListedColormap(["cyan", "darkcyan",
                                      "green", "lime",
                                      "yellow", "gold", "goldenrod",
                                      "darkred", "brown", "red",
                                      "darkviolet"])
    cmap.set_over("indigo")
    cmap.set_under('white')
    bounds = [0.1, 0.5, 1, 2, 3, 4, 5, 6, 8, 10, 20, 40]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    im = ax.imshow(crain, transform=PlateCarree, origin='upper',
                   extent=[70, 139.95, 15, 59.95],
                   cmap=cmap, norm=norm, aspect=1.2)
    cb = fig.colorbar(im, ax=ax, extend="both", extendrect=True, ticks=bounds,
                      extendfrac="auto", pad=0.01, shrink=0.8,
                      aspect=40, fraction=0.01)
    cb.set_label("mm")
    ax.set_xlim((72, 135))
    ax.set_ylim((18, 55))
    ax.set_xticks(list(range(75, 136, 5)), PlateCarree)
    ax.set_yticks(list(range(20, 56, 5)), PlateCarree)
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.set_title("中国自动站与CMORPH降水产品融合的逐小时降水量", fontproperties=font,
                 fontsize=23)
    plt.text(1, -0.07, "公众号 碎积云", fontproperties=font, transform=ax.transAxes,
             horizontalalignment="right", verticalalignment="top", fontsize=14)
    plt.text(0.5, 0.98, "2018-08-17 07:00(GMT)", fontproperties=font,
             transform=ax.transAxes, horizontalalignment="center",
             verticalalignment="top", fontsize=15)
    southsea = plt.imread(r"..\data\map\南海诸岛插图.tif")
    y, x = southsea.shape[:2]
    ax.imshow(southsea, origin='upper', extent=[135-10, 135, 18, 18+10/x*y],
              aspect=1.2)
    plt.show()
    plt.savefig(r"..\data\SURF_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10\demo.png")
