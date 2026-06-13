# STATSGO

GAGES-II 数据集中的土壤属性数据来自于 STATSGO 数据集，参考：[A SOIL SPATIAL DATA FRAMEWORK FOR ENVIRONMENTAL MODELING IN THE CONTIGUOUS US](https://cfpub.epa.gov/si/si_public_record_Report.cfm?Lab=NHEERL&dirEntryId=59726&CFID=78305851&CFTOKEN=96834336)。

为了对 对流层臭氧暴露和氮沉降对森林和全球变化（soil C pools，land use impacts和water balance modeling）的影响做环境评估，开发了一系列土壤相关数据。

这些空间数据描述了 soil particle size analysis [PSA], organic matter[OM], bulk density [BD], rock fragments [RF], soil depth, soil water retention, organic carbon (OC), N (SN), N availability (as N-mineralization), exchangeable bases, and acidity。

简单补充下相关概念。

- [PSA](https://en.wikipedia.org/wiki/Particle_size_analysis)：即粒子大小的测量或simple partical sizing，是确定size range，或一个powder或液体样本中例子的平均size 的实验室技术或一系列步骤的统称。
- [OM](https://zh.wikipedia.org/wiki/%E6%9C%89%E6%A9%9F%E7%89%A9%E8%B3%AA)：有机物质，是由有机化合物所组成的,来自曾经生活过的生物体,如动物或植物在环境中产生的代谢废物和遗体。这些营养物质的流动在环境中是很重要的，也扮演着水循环中的一个角色。土壤中的有机物质主要来源是动物和植物。例如森林中地面上的枯枝落叶或是木材，这些都通常都被称为有机质。当它们被分解而不能再被辨识时称为土壤有机质。 当有机物质继续被分解成一个稳定的物质，这个物质称为腐殖质。
- [BD](https://en.wikipedia.org/wiki/Bulk_density)：也称为 apparent density或volumetric density，定义是土壤粒子质量除以其所占的总体积，总体积包括粒子体积，粒子间空隙体积 和 孔内体积。土壤孔隙率和组成土壤的 成分和土壤压缩的程度有关。
- [RF](https://en.wikipedia.org/wiki/Rock_fragment)：岩石碎片是一种沙粒大小的颗粒或沙粒。
- [soil depth](https://esdac.jrc.ec.europa.eu/public_path/shared_folder/projects/DIS4ME/indicator_descriptions/soil_depth.htm#:~:text=Soil%20depth%20defines%20the%20root,their%20water%20and%20nutrient%20demands.)：定义了植物满足其水分和养分需求的根系空间和土壤体积。soil water storage capacity和effective rooting depth 和 soil depth 相关。
- [Soil water (retention)](https://en.wikipedia.org/wiki/Soil_water_(retention))：土壤能持一定量的水分。土壤可以保留的最大水量称为field capacity田间持水量，而干燥以至于植物无法从土壤颗粒中吸收剩余水分时称为wilting point枯萎点。avilable water可用水是指植物在田间持水量和枯萎点之间的范围内从土壤中吸收的水分。
- [OC](https://zh.wikipedia.org/wiki/%E6%80%BB%E6%9C%89%E6%9C%BA%E7%A2%B3%E9%87%8F)：以碳的含量表示有机物量的一个指标，常用于检测水质。
- [N-mineralization](https://www.topcropmanager.com/understanding-n-mineralization-10515/#:~:text=Nitrogen%20mineralization%20is%20the%20conversion,dependent%20on%20growing%20season%20weather.)：N-mineralization是将土壤有机质、作物残馀物、粪肥和其他有机改良剂中的有机结合氮转化为无机形式的铵态氮和硝态氮。土壤中微生物做这件事，其和环境条件高度相关，所以一直在变化，因为作物吸收的是无机氮，所以这一过程对作物生长很关键。
- [exchangeable bases](https://acsess.onlinelibrary.wiley.com/doi/pdf/10.2134/agronmonogr9.2.c7#:~:text=Exchangeable%20bases%20are%20commonly%20defined,ions%20in%20the%20soil%20solution.)：exchangeable bases通常被定义为附着在粘土和土壤有机成分上的碱土和碱土金属(主要是钙、镁、钾和钠)，它们可以相互交换，也可以在土壤溶液中与其他正离子交换
- [soil pH](https://zh.wikipedia.org/wiki/%E5%9C%9F%E5%A3%A4pH%E5%80%BC)：土壤pH值是衡量土壤中酸度或碱度所代表的意义。是溶液中氢离子活度的一种标度，也就是通常意义上溶液酸碱程度的衡量标准。土壤pH被认为是土壤中的主要变量，因为它控制发生的许多化学过程。它通过控制营养物的化学形式特异性地影响植物营养物的可用性。大多数植物的最佳pH范围在5.5和7.0之间，也有许多植物已经适应在该范围之外的pH值下生长。

这些数据集提供了C和N pool size等的直接信息，而这些也是水文和vegetation 模型的输入数据。地理基础是比例尺1：250000的USDA Natural Resources Conservation Service (NRCS) STATSGO 数据库，STATSGO数据库可以通过map unit component 和 STATSGO tabular 数据连接起来，或者通过components的土壤分类和土壤实验室测量连接起来。

 STATSGO tabular 数据用来开发  PSA, BD, OM, RF, soil depth, salinity, carbonates, gypsum, depth to impermeable layers, and water holding capacity (WHC) 数据集，并对矿质土、有机土、杂区和水的面积范围进行了估计。