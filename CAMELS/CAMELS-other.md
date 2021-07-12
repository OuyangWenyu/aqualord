# 各国的CAMELS数据集

在谷歌的[Dataset Search](https://datasetsearch.research.google.com/)中查询了各国的CAMELS数据集,获得了介绍美国（US)、巴西（BR)、澳大利亚（AUS)、英国（GB）、智利（CL）的文章。

其中:CAMELS-US见文献[The CAMELS data set: catchment attributes and meteorology for large-sample studies](https://doi.org/10.5194/hess-21-5293-2017)

CAMELS-BR见文献[CAMELS-BR: Hydrometeorological time series and landscape attributes for 897 catchments in Brazil - link to files](https://doi.org/10.5194/essd-12-2075-2020)

CAMELS-AUS见文献[CAMELS-AUS: Hydrometeorological time series and landscape attributes for 222 catchments in Australia](https://essd.copernicus.org/preprints/essd-2020-228/)

CAMELS-GB见文献[CAMELS-GB: Hydrometeorological time series and landscape attributes for 671 catchments in Great Britain](https://doi.org/10.5194/essd-2020-49)

CAMELS-CL见文献[The CAMELS-CL dataset: catchment attributes and meteorology for large sample studies – Chile dataset](https://doi.org/10.5194/hess-22-5817-2018)

其实国内也有不完全包括径流数据的CAMELS数据集(CAMELS-CN),详解见文献[Catchment attributes and meteorology for large sample study in contiguous China](https://doi.org/10.5194/essd-2021-71)

这里简要整理下几篇数据集的主要内容,其中CAMELS-US在[CAMELS.md](https://github.com/OuyangWenyu/aqualord/blob/master/CAMELS/CAMELS.md)中已介绍过，将不再赘述。

## CAMELS-BR

该数据集包括：

- 来自3679个流量计的每日流水时间系列
- **897 个**选定流域的气象forcing（降水、蒸发和温度）
- 65个属性，涵盖地形、气候、水文、土地覆盖、地质、土壤和人类干预变量以及数据质量指标

CAMELS-BR将有助于探索集水行为的驱动因素，预测水文变化，并研究人类活动对水循环的影响。

CAMELS-BR可在(https://doi.org/10.5281/zenodo.3709337) 免费获得。

![CAMELS-BR](./image/CAMELS-BR.png "CAMELS-BR" )

## CAMELS-AUS

该数据集包括：

- **222个**不受管制的流域的数据和长期监测
- 水文气象时间序列数据(流量和18个气候变量)
- 与地质、地形、土地覆盖、人为影响、水文气候相关的134个属性，较为特别的属性有：量化人口、植物生长指数和净初级生产力统计

该数据集

1）对大多数流域(75%)提供了评级曲线不确定性估计，并包括多个大气数据集，提供了forcing不确定性的见解；  
2）与来自美国和智利的CAMEL数据集的干旱流域数据相结合，为干旱区水文研究提供了前所未有的资源。

CAMELS-AUS可以从(https://doi.pangaea.de/10.1594/PANGAEA.921850) 免费下载。

![CAMELS-AUS](./image/CAMELS-AUS.png "CAMELS-AUS" )

## CAMELS-GB

该数据集是英国第一个大样本、开源的流域水文数据集

1）整理了来自英国国家河流流量档案（NRFA）的河流流量、流域属性和流域边界，以及一套新的气象时间序列和流域属性;  
2）导出了人类管理属性(包括总结每个流域的取水、回水和水库容量的属性)，以及描述流量数据质量的属性，包括英国的第一组流量不确定性估计;  
3）描述了水流时间序列的不确定性；  
4）提供了新的机会来探索不同的流域特征如何控制河流流量行为，开发用于区域和国家尺度的模型评估和基准的通用框架，并分析整个英国的水文变异性。

该数据集包括：

- **671个**流域的数据，这些流域涵盖了整个英国的各种气候、水文和人类管理属性
- 1970-2015年的日时间序列(包括几个水文极端事件)，包括一系列水文气象变量，降雨、潜在蒸散、温度、辐射、湿度和河流流量

需要注意的是：

1）CAMELS-GB的气候指数是根据CAMELS-GB的完整气象时间序列计算的(1970年10月1日至2015年9月30日的)，而CAMELS和CAMELS-CL都使用1990年至2009年；  
2）在比较跨流域的水文特征时，考虑流量时间序列的长度和缺失数据的百分比；  
3）CAMELS-GB提供的土地覆盖属性不同于使用LCM2000和不同土地利用分组的NRFA网站提供的。

CAMELS-GB可在(https://doi.org/10.5285/8344e4f3-d2ea-44f5-8afa-86d2987543a9) 获得。

![CAMELS-GB](./image/CAMELS-GB.png "CAMELS-GB" )

## CAMELS-CL

该数据集包括：

- **516个**流域，对于每个流域，数据集提供流域边界（克服了官方国家水文网络的主要限制）、每日流水记录和盆地平均每日降水时间系列、最大、最小和平均温度、潜在蒸发（PET）和SWE
- 气候、地形、地质、土地覆盖等流域属性

该数据集

1）依靠该国公开的水库和水权数据，估计了流域内的人类干预程度；  
2）综合了多样化和互补的数据集，计算了 70 个流域属性，这些属性描述了地形、地质、土地覆盖、气候、水文和人类干预；  
3）通过评估（1）两个关键气象变量（降水和PET）的不确定性和（2）人类干预对流域响应的影响，展示该数据集如何有助于增进我们对水文系统及其可预测性的理解；  
4）提供SWE估算。

CAMELS-CL可用于解决与流域分类、相似性和区域化、模型参数估计、径流生成的主导控制、不同土地覆盖类型对流域响应的影响、干旱历史和预测特征以及气候变化对水文过程的影响相关的研究问题。

CAMELS-CL可在(https://doi.pangaea.de/10.1594/PANGAEA.894885) 下载。

![CAMELS-CL](./image/CAMELS-CL.png "CAMELS-CL" )

## CAMELS-CN

该数据集是中国大陆首个大尺度流域属性和气象时间序列数据集，也是我国首个面向流域的静态属性数据集，所研究的流域是**从基于全球流域数据集的数字高程模型（DEM）中得到**的中国大陆地区的**4875个流域**。与之前提出的数据集相比，该数据集
- 提取了更多的流域特征，产生125个属性，提供了一个完整的流域描述
- 提出了覆盖黄河流域102个流域的水文数据集Normal-Camels-YR

该数据集主要包括：

- 土壤、土地覆盖、气候、地形、地质等120多个流域属性
- 基于质量控制的站点观测数据集SURF_CLI_CHN_MUL_DAY提出的**29年气象时间序列(1990 - 2018年)**

![CAMELS-CN](./image/CAMELS-CN.png "CAMELS-CN" )

各属性介绍：

- 气候指数  

  气象原始数据由[中国气象数据网](http://data.cma.cn)的[SURF_CLI_CHN_MUL_DAY (V3.0)数据集](http://data.cma.cn/data/cdcdetail/dataCode/SURF_CLI_CHN_MUL_DAY_V3.0.html)提供，采用反距离加权法对现场观测数据进行插值，然后，通过对插值栅格的流域尺度提取取平均值，得到气候指数
  
![CN-Climate indices](./image/CN-Climate.png "CN-Climate indices" )

- 地质  

  为描述每个流域的岩性特征，使用了相同的两个全球数据集CAMELS，全球岩性图(GLiM)和全球水文地质图(GLHYMPS)  
  
  GLiM提供由现有区域地质图组装而成的高分辨率全球岩性图，用1235400个多边形表示，多边形转换为栅格格式，用于盆地规模的岩性类型统计。
  
  GLHYMPS提供了对地下渗透率和孔隙度的全球估算，这是土壤水文分类的两个关键特征，GLHYMPS可以区分细粒和粗粒沉积物和沉积岩，基于高分辨率的GLiM地图，GLHYMPS根据不同岩石类型的渗透率来确定地下渗透率。对于提出的数据集，我们计算了孔隙度的流域算术平均值。随后，采用对数尺度的几何平均值来代表地下渗透率。
  
  孔隙度和渗透率的分布与地质类别相似。这两种特征高度依赖于岩石性质，松散沉积物、混合沉积岩、硅质碎屑沉积岩、碳酸沉积岩和酸性深成岩是中国大陆最常见的五种地质类型。

![CN-Geology](./image/CN-Geology.png "CN-Geology" )

- 土地覆盖  

  选择了两个表征地表植被密度和生长的指标:归一化植被指数(NDVI)和叶面积指数(LAI)
 
  NDVI是用来评估被观测区域是否有绿色活植被或植物的健康状况的指标，有效范围为-0.2~1。而NDVI只是植被密度的一种定性度量，不能提供该地区植被密度的定量估计。此外，NDVI往往提供不准确的植被密度测量，只有长期的测量和比较才能保证其准确性。仅用NDVI不足以估计一个地区的植物状况。因此，选择LAI来补充NDVI的不足。
  
  LAI定义为单位地面面积的总针表面积和单位地面面积的整个针表面积的一半。它是一个可量化的值，在功能上与许多水文过程有关，如截水。使用的数据源为NDVI的Terra中分辨率成像光谱仪(MODIS)植被指数和LAI的中分辨率成像光谱仪(MODIS)。其中，最大月LAI作为表征植被截留能力的指标，最大蒸发能力以及最大和最小月LAI的差值，代表了LAI的时间变化。
  土地覆盖分类是指基于遥感影像将地面分割成不同的类别。数据集的构建采用国际地圈-生物圈计划(IGBP)年度分类，由c4.5决策树算法导出。
  
  利用双参数方法，基于IGBP分类计算了每个流域的平均生根深度(50%和90%)。植被根系深度的分布影响着地表的持水能力和表土层的年蒸散量。许多模型将根系深度作为表征土壤吸湿能力的重要参数。

![CN-Landover](./image/CN-Landover.png "CN-Landover" )

- 位置和地形  

  流域边界文件来自全球流域数据集。PDBD数据集来源于高分辨率(100m-1km)的数字高程模型(DEM)，误差通过自动方法或人工方法进行校正。
  
  PDBD提供了流域的人口和人口密度估计数，这两个指标也包括在CAMELS-CN中，作为人类干预的衡量标准。利用全球径流数据中心(Center 2005)的流量监测站来参考导出的流域。在中国大陆地区，PDBD具有较高的平均匹配面积率(AMAR)，与现有全球流域数据具有良好的地理一致性。
  
  每个流域的地形属性根据从[陆地过程分布式活动档案中心（LP DAAC）](https://lpdaac.usgs.gov)检索的ASTGTM产品确定。
  
  CAMELS数据集只提供了两个参数(两个面积估计)来描述流域形状，为提供完整描述，计算了与径流过程相关的几个流域几何参数，包括流域形态因子、形状因子、紧实系数、循环比和延伸比。
  
![CN-topography](./image/CN-topography.png "CN-topography" )
  
- 土壤

  该数据集共有54个土壤属性，来源于(Hengl, Mendes de Jesus et al. 2017)， (Dai, Xin et al. 2019)和(Shangguan, Dai et al. 2013)。

![CN-Soil](./image/CN-Soil.png "CN-Soil" )

- 气象时间序列  

  面向流域的数据集基于中国气象数据网，提供了1990-2018年4875个流域的气象时间序列。气象变量包括压力、温度、相对湿度、降水量、蒸散发、风速、日照时数、地表温度和潜在蒸散量。
  
  1951-2010年的气象时间序列数据是根据“1951-2010年中国国家地面站数据修正月数据文件基础数据采集”数据建设项目得到的。其他数据包括各省向国家气象信息中心每月报告的数据，以及自动地面站每小时和每天实时上传的数据。对SURF_CLI_CHN_MUL_DAY数据集进行了质量控制，各变量的质量和完整性较以往同类产品有明显提高。在数据集的开发过程中，通过反距离加权插值其最近的站点来填充缺失的数据。
  
  由于早期站点分布稀疏，我们仅使用1990 - 2018年的记录来构建数据集，以确保数据质量。利用开源rasterio软件包从插值的国家栅格中提取流域级栅格。对于所有变量，我们取提取的流域栅格上的算术平均值作为流域平均值。利用Penman方程和其他流域气象变量估算潜在蒸散量。
  

**Normal-Camels-YR数据集**

在该数据集开发过程中，删除了观测量过少的盆地，导致盆地标识不连续。Normal-Camels-YR涵盖黄河流域的102个测量仪表，为每个流域提供流域边界形状文件、静态属性和标准化的径流测量。

径流测量的时间分辨率为7天，径流测量记录的平均长度为684，这意味着每个流域径流测量的平均周期超过13年。Normal-Camels-YR所包含的气象变量略有不同;它引入了一些变量的每日最大值和最小值。

CAMELS-CN与Normal-Camels-YR相结合，有助于探索不同流域特征对水文行为的影响，了解不同流域间的水文行为迁移，并为中国大尺度模型评估和基准提供通用框架。

CAMELS-CN可从(http://doi.org/10.5281/zenodo.4704017) 免费获得。