# Data for WRM

本项目参考[Satellite Remote Sensing for Water Resources Management: Potential for Supporting Sustainable Development in Data-Poor Regions](https://doi.org/10.1029/2017WR022437)等文献，以及[Applied Remote Sensing Training](https://arset.gsfc.nasa.gov/)等资料，总结平时接触到的有可能用于Water Resources Management(WRM)的数据资源，主要记录数据的来源，和下载获取方式，如果有些数据自己实际使用了，也会记录相关的数据处理方法，关于数据的更多文献解读如有必要会记录到elks项目的文献部分，这里不重点介绍。

*日常积累，持续更新...*

## 主要内容

目前主要内容如下：

- ARSET
- CAMELS
- cloud storage：从各类云端存储下载数据，比如kaggle，box，google drive等
- daymet
- GAGES
- GRACE
- LDAS
- National Hydrography
- CHINA RADAR precipitation
- SMAP

需要的软件包如下：

```Shell
conda install -c conda-forge kaggle, pydrive, xarray, netcdf4, matplotlib, gdal, future, wxpython
pip install wget
pip install pyModis
```

可以执行以下代码安装环境：

```Shell
conda create --prefix ./envs python=3.7
conda activate xxx\aqualord\envs
conda install -c conda-forge jupyterlab
conda install -c conda-forge kaggle, pydrive, xarray, netcdf4, matplotlib, gdal, future, wxpython
pip install wget
pip install pyModis
conda env export > environment.yml
```

## 参与贡献

1. Fork 本项目
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request
