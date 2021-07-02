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

## CAMELS-AUS

该数据集包括：

- **222个**不受管制的流域的数据和长期监测
- 水文气象时间序列数据(流量和18个气候变量)
- 与地质、地形、土地覆盖、人为影响、水文气候相关的134个属性，较为特别的属性有：量化人口、植物生长指数和净初级生产力统计

该数据集

1）对大多数流域(75%)提供了评级曲线不确定性估计，并包括多个大气数据集，提供了forcing不确定性的见解；

2）与来自美国和智利的CAMEL数据集的干旱流域数据相结合，为干旱区水文研究提供了前所未有的资源。

CAMELS-AUS可以从(https://doi.pangaea.de/10.1594/PANGAEA.921850)  免费下载。

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

## CAMELS-CN

该数据集是中国大陆首个大尺度流域属性和气象时间序列数据集，也是我国首个面向流域的静态属性数据集，所研究的流域是从数字高程模型中得到的中国大陆地区的**4875个流域**。与之前提出的数据集相比，该数据集
- 提取了更多的流域特征，产生125个属性，提供了一个完整的流域描述
- 提出了覆盖黄河流域102个流域的水文数据集Normal-Camels-YR

该数据集主要包括：

- 土壤、土地覆盖、气候、地形、地质等120多个流域属性
- 基于质量控制的站点观测数据集SURF_CLI_CHN_MUL_DAY提出的**29年气象时间序列(1990 - 2018年)**
  包括压力、温度、相对湿度、降水量、蒸发量、风速、日照时数、地表温度和潜在蒸散发。
  在数据集的开发过程中，通过插值其最近的站点来填充缺失的数据，对于所有变量，我们取提取的流域栅格上的算术平均值作为流域平均值。利用Penman方程和其他流域气象变量估算潜在蒸散量。

**Normal-Camels-YR数据集**

在该数据集开发过程中，删除了观测量过少的盆地，导致盆地标识不连续。Normal-Camels-YR涵盖黄河流域的102个测量仪表，为每个流域提供流域边界形状文件、静态属性和标准化的径流测量。
径流测量的时间分辨率为7天，径流测量记录的平均长度为684，这意味着每个流域径流测量的平均周期超过13年。Normal-Camels-YR所包含的气象变量略有不同;它引入了一些变量的每日最大值和最小值。

CAMELS-CN可从(http://doi.org/10.5281/zenodo.4704017) 获得。