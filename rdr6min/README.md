# 国家气象信息中心数据

结合日常所需及现存项目（目前主要参考：[py-nmic](https://github.com/Mo-Dabao/pyNMIC)，一些[博客资源](https://blog.csdn.net/qq_21567935/article/details/88828112)），本项目旨在构建一个方便获取国家气象信息中心雷达测雨数据的工具包。

## 主要内容

搞一搞[国家气象信息中心（National Meteorological Information Center）](https://data.cma.cn/)雷达测雨数据。由于中国气象数据网上每次选择完数据之后，需要等待打包的时间较长（大约需要1小时），且数据的后处理比较麻烦，所以有必要开展爬虫及数据处理工作。首先半自动式爬虫获取数据，然后再逐步改进到全自动的。

## 开发环境

``` python
anaconda                  5.3.1
python                    3.7.2
```

第三方库：

``` python库
h5py                      2.9.0
numpy                     1.16.2
matplotlib                3.0.2
astropy                   3.1.2
```
