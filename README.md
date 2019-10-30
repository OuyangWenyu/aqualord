# 国家气象信息中心数据

结合日常所需及现存项目（目前主要参考：[py-nmic](https://github.com/Mo-Dabao/pyNMIC)，一些[博客资源](https://blog.csdn.net/qq_21567935/article/details/88828112)），本项目旨在构建一个方便获取国家气象信息中心数据的工具包。

## 主要内容

搞一搞[国家气象信息中心（National Meteorological Information Center）](https://data.cma.cn/)。目前内容主要有：

### 风云卫星云图数据

[FY-4A](./FY4A)

2019-3-14：
- 不是是`pyshp`还是`Cartopy`更新后`Cartopy`无法打开含`gbk`编码的shp文件，所以把shp文件处理成utf-8的编码了
- 改变了文件目录结构

2018-12-9：
- 新增GUI(tkinter)，比较痛苦，显然不爱写界面的东西
- 面向对象重构`extract.py`为`fy4a.py`，感觉还行
- `test.py`没有同步更新
- 缺测值没有处理，一旦选定范围有缺测值就无法定标、出结果
- 信息显示有待完善（时间、文件名等）
- 图片工具条用的`matplotlib`自带的，方便但可能不好看、不好用
- 想尝试类似`jupyter notebook`那种和浏览器结合起来的交互界面

![截图](../data/fy4a/截图.png)
<center>界面截图</center><br>


2018-11-20：<br>
- 大量更新
- 放弃经纬度查找表，通过公式进行经纬度行列号互转

<center>

![Tbb云顶亮温（Channel12）](../data/fy4a/Tbb云顶亮温（Channel12）.png)
Tbb云顶亮温（Channel12）</center><br>
<center>

![REGC大致范围](../data/fy4a/REGC大致范围.png)
REGC大致范围</center>


2018-11-08：<br>
国家卫星气象中心官网上提供的经纬度查找表有问题（至少4km的有问题）：
- `FY-4A数据行列号和经纬度的互相转换方法`中的`查表方法`教程pdf中说`高字节在前`其实是在后即小端存储格式；`前8字节为经度值，后8字节为纬度值`也说反了
- .gz文件应该不是标准的.gz格式，导致用gzip包无法直接打开，用7z手动解压也会提示`有效数据外包含额外数据`
- 官网提供的经纬度与行列号互转公式中星下点经度在不同情况下有时是弧度制有时是角度制千万注意

### 雷达测雨数据

获取雷达测雨图并解码数据，获取雷达降雨数据的目的是想看看能否利用其空间信息获取全面的特点，提高降雨观测精度，以使流域径流预报有更准确的输入，为此，项目还提供了降雨观测融合算法。

由于中国气象数据网上每次选择完数据之后，需要等待打包的时间较长（大约需要1小时），且数据的后处理比较麻烦，所以开展爬虫及数据处理工作。首先半自动式爬虫获取数据，然后再逐步改进到全自动的。fy4a和surf_cli_chn_merge_cmp_pre_hour_grid_0.10目前只包括对示例数据的读取。

### 中国自动站与CMORPH降水产品融合的逐时降水量网格数据集（1.0版）数据

 [中国自动站与CMORPH融合的逐时降水量0.1°网格数据集（1.0版）](http://data.cma.cn/data/cdcdetail/dataCode/SEVP_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10.html)

`SURF_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10`

`reader.py`中的`read()`即为用于读取该产品的函数。

---

根据提供的.ctl文件：
```
DSET ^SEVP_CLI_CHN_MERGE_FY2_PRE_HOUR_GRID_0.10-%y4%m2%d2%h2.grd
*
UNDEF -999.0
*
OPTIONS   little_endian  template
*
TITLE  China Hourly Merged Precipitation Analysis
*
xdef  700 linear  70.05  0.10
*
ydef  440 linear  15.05  0.10 
*
ZDEF     1 LEVELS 1  
*
TDEF 9999 LINEAR 00Z01Aug2010 1hr 
*
VARS 2                           
crain      1 00  CH01   combined analysis (mm/Hour)
gsamp      1 00  CH02   gauge numbers
ENDVARS
```

可直接获得信息：
- 存储方式是小端存储
- 空间范围为：70.05°E\~139.95°E，15.05°N\~58.95°N，间隔0.1°
- 有两个变量：降雨量`crain`和雨量计数量`gsamp`

可推测而得的信息：
- 结合文件的大小为2464000字节，可推测每个数据为`2464000/(700*440*2)`=4字节
- 结合示例图图例可知数据应该是浮点数（没有找到数据类型的描述）

需要注意的是：
- 经过尝试，数组存储顺序是右侧为先（C-like）
- 数据的存储顺序是自西向东、自南向北、自`crain`向`gsamp`，直接读取时矩阵为上南下北，为了方便绘图等操作已经按习惯调整为上北下南

出图如下：

![demo](../data/surf_cli_chn_merge_cmp_pre_hour_grid_0.10/demo.png)

官网原图：
![map](../data/surf_cli_chn_merge_cmp_pre_hour_grid_0.10/surf_cli_chn_merge_cmp_pre_hour_grid_0.10SURF_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10-2018081707.gif)

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

## 参与贡献

1. Fork 本项目
2. 新建 hydar_xxx 分支 (xxx可以是您的名称ID)
3. 提交代码
4. 新建 Pull Request
