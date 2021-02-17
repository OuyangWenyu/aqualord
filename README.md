# Data for WRM

本项目参考[Satellite Remote Sensing for Water Resources Management: Potential for Supporting Sustainable Development in Data-Poor Regions](https://doi.org/10.1029/2017WR022437)等文献，以及[Applied Remote Sensing Training](https://arset.gsfc.nasa.gov/)等资料，总结平时接触到的有可能用于Water Resources Management(WRM)的数据资源，主要记录数据的来源，和下载获取方式，如果有些数据自己实际使用了，也会记录相关的数据处理方法，关于数据的更多文献解读如有必要会记录到elks项目的文献部分，这里不重点介绍。

## 主要内容

目前主要内容如下（*日常积累，持续更新*）：

- ARSET：NASA的卫星遥感数据使用教程
- CAMELS：衡量水文模型性能常用数据集
- CloudStor：记录从各类云端存储下载数据的方法，比如kaggle，box，google drive等
- DAM: 大坝水库相关数据集
- DataFormat：常见数据格式
- daymet：一个气象forcing数据集
- EOMarket：一个汇总地理空间数据及应用的平台
- GAGES：USGS的径流数据集
- GRACE：重力卫星数据
- ICESat：主要关注其在内陆水体测量方面的数据
- Landsat：主要关注内陆水体表面识别方面
- LDAS：NASA陆面同化系统数据
- MODIS：MODIS 相关数据集多，用途广泛
- NH：美国National Hydrography基础数据
- rdr6min：国内气象网站下载的雷达测雨数据
- SMAP：NASA测土壤含水量卫星的数据

用到的软件包如下：

```Shell
conda: python=3.7, jupyterlab kaggle, pydrive, xarray, netcdf4, matplotlib, gdal, future, wxpython
pip: wget, pyModis
```

可以在本项目根目录下执行以下代码安装环境：

```Shell
conda env create -f environment.yml
```

## 参与贡献

1. Fork 本项目
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request
