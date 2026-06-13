# 水库数据

这里收集整理一些关于水库数据集的情况。

## 1

来自世界银行的 Dam 和 reservoir 数据，可见于 NASA 的社会经济数据库 Socioeconomic Data and Applications Center (sedac) 的 [Global Reservoir and Dam (GRanD)](https://sedac.ciesin.columbia.edu/data/set/grand-v1-dams-rev01) 。

该数据集提供了水库的地理信息。GRanD包括了6862个水库和它们的大坝的记录，水库的形状是根据高空间分辨率的遥感图像提取的，有相应shp文件。水库的属性就只有水库的面积。相关的大坝数据包括大坝和被蓄水河流的名称，主要用途，最近的城市，面积和建造年份。虽然主要目的是涵盖库容大于 0.1 立方公里的水库，但是对有数据的小水库，也会纳入其中。更多的数据信息可以参考文献：[Global Reservoir and Dam Database, Version 1 (GRanDv1): Reservoirs, Revision 01.](https://doi.org/10.7927/H4HH6H08) 和 [ High-Resolution Mapping of the World's Reservoirs and Dams for Sustainable River-Flow Management](http://dx.doi.org/10.1890/100125)。

简单总结下第二篇文献的内容，这篇文章的很多结论还是很有启示意义的。

首先，现状是世界上很多河流都已经有水库建设了，数据上，大水库拦蓄了相当于1/6的入海水的蓄水量，还有很多统计不到的小水库。这些水库给人类带来了很多好处，比如，约15%左右的粮食得益于大水库的建设，约20%电量是水电；当然也带来一些问题，比如环境生态问题。因此需要分析水库的影响，所以需要水库的数据，这就是这篇文章的motivation。

数据集就是上面提到的数据集。包括的内容主要有：水库的名称，空间坐标，建设年份，表面积，库容，大坝高度，main purpose，和高度。通过关联 GRanD 和 HydroSHEDS，可以得到上下游的topology，这种关联还能帮助分析每个水库的流域面积，估计水库位置的长期平均径流。

然后文章还有一些比较有意思的工作，首先是DOR，即 cumulative upstream storage in percent of average flow. 高 DOR 值表示越多的径流会被水库坦化，即更大的调节库容。尤其是DOR 大于100% 的，那基本上河流就完全变成人工模式了。还有些水库比如三峡，虽然DOR不大，但是对径流影响非常大。DOR>=2%都是有影响的。

然后一些比较general的结论： 河流的size对水库径流调节作用是有影响的；DOR是很重要的因素；水库本身的调度模式也有很大影响。

还有一些可以探讨的问题：河段尺度的影响的全球分布；流域内水库大坝的相对影响；中小尺度流域内的影响等。还有其他相关数据也可以补充进GRanD集。

## 2

来自USGS 的 水库形态数据库 RMD， 参考：[A Reservoir Morphology Database for the Conterminous United States](https://www.sciencebase.gov/catalog/item/587fb41ae4b085de6c11f38b)。

The U.S. Geological Survey, in cooperation with the Reservoir Fisheries Habitat Partnership, combined multiple national databases for the purpose of calculating new morphological metrics for 3,828 reservoirs over 250 acres in surface area. These new metrics include, but are not limited to, shoreline development index, index of basin permanence, development of volume and other descriptive metrics based on established morphometric formulas. The new database also contains modeled chemical metrics from the SPARROW model and physical metrics such as surface area, storage, hydraulic height, etc. Because of the nature of the existing databases used to compile the Reservoir Morphology Database the inherent missing data, some metrics were not populated when data was missing. Location of individual dams was removed from the database due to its sensitive nature. The Reservoir Morphology Database will assist reservoir managers in characterizing reservoirs throughout the continental United States with the calculated morphological parameters contained within. The accompanying data series report entitled "A Reservoir Morphology Database for the Conterminous United States" (DOI Number) contains methods of database constructions and metric calculation. 

Understanding conditions and trends in the Nation’s lakes and reservoirs requires information on reservoir morphology and water chemistry. Data pertaining to different aspects of reservoir morphology and water chemistry are contained in databases developed by multiple agencies for different purposes. In particular, the National Inventory of Dams (NID) (U.S. Army Corps of Engineers, 1998), the National Hydrography Dataset (NHD) (Simley and Carswell, 2009), the Enhanced River Reach File (ERF1_2) (Nolan and others, 2002), the SPAtially Referenced Regressions on Watershed (SPARROW) model (Schwarz and others, 2006) collectively comprise datasets, which combined would support national and broad regional analysis of reservoirs in the United States. In 2010, the U.S. Geological Survey (USGS) began an effort to compile a national database containing physical, modeled chemical, and morphological metrics for reservoirs with surface areas of at least 250 acres. The resulting database, hereafter known as the Reservoir Morphology Database (RMD), can be used by natural resource managers in assessing reservoir characteristics throughout the conterminous United States.

## 3

两个来自 Huilin Gao 的数据源，可以参见[Huilin Gao Dataverse (Texas A and M University)](https://dataverse.tdl.org/dataverse/HGao)

其一是：[Replication Data for: CONUS Reservoir Evaporation Dataset (CRED)](https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/S8CJ7X)

By fusing remote sensing and modeling approaches, this study developed a novel method to accurately estimate the evaporation losses from 721 reservoirs in the contiguous United States (CONUS). Reservoir surface areas were extracted and enhanced from the Landsat based Global Surface Water Dataset (GSWD) from March 1984 to October 2015. The evaporation rate was modeled using the Penman Equation in which the lake heat storage term was considered. The evaporation volume was calculated as the product of the reservoir area and evaporation rate.

第二个：[Global Reservoir Surface Area Dataset (GRSAD)](https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/DF80WG)

This dataset contains the time series of area values for 6817 global reservoirs (with an integrated capacity of 6099 km3) generated from 1984 to 2015. It was based on the dataset by Pekel et al. (2016), with the contaminations from clouds, cloud shadows, and terrain shadows corrected automatically.

## 4

一个 global 的 storage-area-depth 关系数据集，可以参见：[Global Reservoir Geometry Database](https://wowuoh.wixsite.com/home/models-data)。 数据集制作方式可以参考文献：[A New Global Storage‐Area‐Depth Data Set for Modeling Reservoirs in Land Surface and Earth System Models]( https://doi.org/10.1029/2017WR022040)

这里简单归纳下这篇文献的大概内容，这篇文章目的是为了获取全球水库的库容面积深度关系，基于来自GRanD数据库中超过6800个水库和HydroLAKES的70个水库，还有Global Lake and Wetland Database 和 Dams, Lakes and Reservoirs Database for the World Water Development Report II 两个数据集的基本信息数据制作。用来自Gao和Zhang根据遥感影像计算的库容面积高度关系以及来自USGS等机构人员的水库库容水位关系做验证。

基本方法是先设置一些简化的几何模型，然后根据数据集数据对各水库筛选出最优的shape，再根据各个shape的基本几何关系推求出S－A－D关系。

最后结果有70%的水库总库容误差都在5%以内，85%的误差在25%以内。另一些比较有意思的结论，其一，主要用途为发电，灌溉和供水的水库用常规的几何形状就能很好表示；另外，大部分水库都是用Rectangular‐Prism 形状较好。

## 5

GOODD是一个新的全球大坝和水库的数据库，主要参考：[GOODD, a global dataset of more than 38,000 georeferenced dams](https://www.nature.com/articles/s41597-020-0362-5)，数据集可见于：[Global Dam Watch](http://globaldamwatch.org/)，该数据库中有水库的经纬度坐标和上游的shape图，不过它不是直接公开的，需要发送申请给数据制作方。其制作过程简单描述如下。

首先，从几个现有的大坝数据库中提取数据，然后再通过国际合作，找到更多的数据，作为GOODD数据库的一部分，数据来源很多，详情可见原文。然后再通过google earth和SRTM 的 水体数据集SWBD 来辅助数字化过程。 

中间设置有最小可识别的水库大坝尺寸标准，即在低分辨率的遥感影像下（LANDSAT Geocover 2000）仍能识别的大坝最小尺寸就是标准。最后得到的是500m长水库和150m长大坝是最低标准。

大坝确认好之后，就进行上游流域的识别。首先使用了HydroSHEDS DEM + PCRaster D8算法，先得到了一个粗糙的径流网络，然后再通过每个大坝每个大坝的人工检查来确定好合适的位置。 所有大坝位置都配准到河流网络上之后，再使用PCRaster来识别大坝上游流域。

制作大致过程就是上面这样。然后再对大坝的数量，流域的范围进行验证。


## 6

一个美国陆军工程兵团的大坝数据库：[National Inventory of Dams More than 90,000 dams nation-wide](http://nid.usace.army.mil/)

老网站可能访问不通了，新网站可以查看这里：[National Inventory of Dams](https://damsdev.net/#/)

读取可以参考本文件夹下另外两个jupyter文件，主要使用了[HyRiver](https://hyriver.readthedocs.io/en/latest/)，不过USACE的网站老是连不上，所以这块程序经常挂掉。

选择 “academic” 可以看到网页，然后选择下载即可下载数据了。可以利用下面的链接下载： https://nid.sec.usace.army.mil/ords/NID_R.DOWNLOADFILE?InFileName=NID2018.xlsx 2018年的总的统计数据。

把InFileName 的值换成以下内容可下载特定州的：

AL
AR
AZ
CA
CO
CT
DE
FL
GA
GU
HI
IA
ID
IL
IN
KS
KY
LA
MA
MD
ME
MI
MN
MO
MS
MT
NC
ND
NE
NH
NJ
NM
NV
NY
OH
OK
OR
PA
PR
RI
SC
SD
TN
TX
UT
VA
VT
WA
WI
WV
WY

现在看下数据，点击HELP标签即可查看，Definition下的问号点击即可看到信息，这里记录下一些比较关心的数据。

经度：(Number) Longitude at dam centerline as a single value in decimal degrees, NAD83.
纬度：(Number) Latitude at dam centerline as a single value in decimal degrees, NAD83.
NID-Storage: (Acre-Feet, Number) Calculated field: Maximum value of normal storage and maximum storage. Accepted as the general storage of the dam.
purposes:Enter one or more of the following codes to indicate the current purpose(s) for which the reservoir is used:

- I for Irrigation;
- H for Hydroelectric;
- C for Flood Control and Storm Water Management;
- N for Navigation;
- S for Water Supply;
- R for Recreation;
- P for Fire Protection, Stock, Or Small Farm Pond;
- F for Fish and Wildlife Pond;
- D for Debris Control;
- T for Tailings;
- G for Grade Stabilization;
- O for Other.

The order should indicate the relative decreasing importance of the purpose. Codes are concatenated if the dam has multiple purposes. For example, SCR would indicate the primary purposes, Water Supply, followed by Flood Control and Storm Water Management, and then Recreation.

其下载使用方法可以借助[这里](https://github.com/cheginit/pygeohydro)的代码。

## 7

中国的大坝数据在网上不太容易找到，这里有一个网站：[Spreadsheet of Major Dams in China](https://www.internationalrivers.org/resources/spreadsheet-of-major-dams-in-china-7743)