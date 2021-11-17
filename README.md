# Data for WRM

本项目总结平时接触到的有可能用于Water Resources Management(WRM)的数据资源，主要记录数据的基本情况和下载获取方式，如果有些数据自己实际使用了，也会记录相关的数据处理方法。

参考资料：

- [Satellite Remote Sensing for Water Resources Management: Potential for Supporting Sustainable Development in Data-Poor Regions](https://doi.org/10.1029/2017WR022437)
- [Applied Remote Sensing Training](https://arset.gsfc.nasa.gov/)
- ……

## 主要内容

目前主要内容如下（*日常积累，持续更新*）：

- ARSET：NASA的卫星遥感数据使用教程
- CAMELS：大尺度水文建模常用数据集
- DAM: 大坝水库相关数据集
- DEM：数字高程数据下载
- DataFormat：常见数据格式
- daymet：一个气象forcing数据集，也是CAMELS数据集的数据源之一，介绍如何下载读取使用它
- Electric：电力系统方面与水相关的数据，目前只简单介绍了下美国电网情况
- EOMarket：一个汇总地理空间数据及应用的平台
- GAGES：USGS评价径流的数据集
- GRACE：重力卫星数据，目前只是看论文时候遇到了，简单了解了下
- HydroSHEDS：这是水文领域比较常见的一个公开数据集，目前只是加入它进来，留个坑
- ICESat：主要关注其在内陆水体测量方面的数据，目前只是因为看到了相关论文，简单了解其情况
- Landsat：目前仅简单介绍了下基本情况
- LDAS：NASA陆面同化系统数据
- MODIS：MODIS 产品的简介和基本下载方法
- NH：美国National Hydrography基础数据介绍
- NLCD：美国Land Cover数据库，可以直接通过[HyRiver](https://github.com/cheginit/HyRiver)相关库读取其数据
- SMAP：NASA测土壤含水量卫星的数据，记录其基本情况和下载方法
- WebService：记录从各类云服务下载数据的方法，目前主要是Google drive和Kaggle

## 环境配置

可以在本项目根目录下执行以下代码安装python运行环境（已安装好miniconda或anaconda）：

```Shell
conda env create -f environment.yml
```

## 参与贡献

1. Fork 本项目
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request
