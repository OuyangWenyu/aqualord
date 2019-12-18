# National Hydrography

实际地表水文gis数据的处理过程中会需要不少地理数据，在美国比较常用的有美国国家水文地理数据。参考：[National Hydrography](https://www.usgs.gov/core-science-systems/ngp/national-hydrography)。由于它是美国国家地理空间计划National Geospatial Program (NGP) 的数据集，因此在了解它之前首先，首先认识下整个NGP数据的框架。

## NGP简介

NGP提供了代表美国topography, natural landscape, 和 manmade environment 的数字地理空间数据。NGP数据可以通过The National Map Data Download 访问获取。

NGP包括很多数据集，在[网页](https://www.usgs.gov/core-science-systems/national-geospatial-program)上可以看到，有：

- [Topographic Maps](https://www.usgs.gov/core-science-systems/national-geospatial-program/topographic-maps)：USGS的一个标志性产品，易用又可信任的全美landscape数据。空间分辨率7.5-minute quadrangles，目前有两个产品类型：[US Topo](https://www.usgs.gov/core-science-systems/national-geospatial-program/us-topo-maps-america?qt-science_support_page_related_con=0#qt-science_support_page_related_con)以及 [Historical Topographic Map Collection (HTMC)](https://www.usgs.gov/core-science-systems/ngp/topo-maps/historical-topographic-map-collection?qt-science_support_page_related_con=0#qt-science_support_page_related_con)，前者主要是当前地图，后者主要反映历史情况；
- 3D Elevation：3DEP产品是正在进行制作的产品，使用lidar生成全美的数据，到2023年完成提供第一版的3d高程高分辨率数据；
- National Hydrography：这个是本文重点介绍内容，这里先不展开，详情后续介绍。
- U.S. Board on Geographic Names：联邦政府统一地理命名，BGN 包括联邦政府关心的地理信息，人口，生态和公众徒弟管理等信息。
- The National Map：美国国家地图是NGP的基石，是USGS和其他联邦，州等机构共同合作的结果。可以通过[TNM Viewer](https://viewer.nationalmap.gov/advanced-viewer/) 轻松可视化最近的美国国家地图数据。TNM Supporting Themes包括交通（路，机场，小路，铁路等），建筑（学校，消防站，警察局，医院等），边界（联邦，部落，州，城市村庄等），土地覆盖（基于Landsat的30m分辨率土地利用数据），数字正射影像（和National Agriculture Imagery Program (NAIP)合作的高分辨率航空摄影数据，1m分辨率高精度数据），和小分辨率数据集（退役的旧数据，同时还提供了低分辨率的地图版本）。

更详细情况可以参考：[Datasets](https://viewer.nationalmap.gov/basic/)。

还有一些其他术语简要记录下：

- CEGIS：一个联邦和学术机构科学家组成的虚拟机构，以支持国家地图和3DEP的研究。
- User Engagement：“用户参与办公室”执行与国家地理空间规划的关键举措相关的外联和协调工作。该办事处还在协调地理空间活动以支持紧急反应方面提供局一级的领导，并为阿拉斯加制图倡议提供领导。
- Stewardship and Community：数据集都是由一个强大的社区来维护和更新的。

## NH简介

NGP管理着不同的NH数据集，包括 National Hydrography Dataset (NHD), Watershed Boundary Dataset (WBD), and NHDPlus High Resolution (NHDPlus HR)，这些数据集表示了美国地表水的情况，可用于制图，建模等应用。其中，前两者组成了一个丰富的地理空间数据系列，该系列能反应全美地表水网络和水文流域。NHD，在1:24000及更高（阿拉斯加是1:63,360）的比例尺下表示了全美的大河，小溪，水渠，湖泊，池塘，冰川，海岸线，大坝和径流站以及相关特征。WBD以8个水文单元表示了美国的流域。NHD和WBD是美国最新的水文地理数据集。

NHD和WBD的地址系统与街道邮编编码类似，给了水资源研究创建了一套索引和报告的系统，比如 [Hydrography Event Management (HEM) Tool](https://www.usgs.gov/core-science-systems/ngp/national-hydrography/tools#HEM) 和 [HydroLink Tool](https://maps.usgs.gov/hydrolink/)。不过单独使用NHD或者WBD，这套地址系统不能将径流网络和其临近landscape信息联系起来。因此，为了解决这样一个问题，USGS开发了[NHDPlus High Resolution (NHDPlus HR)](https://www.usgs.gov/core-science-systems/ngp/national-hydrography/nhdplus-high-resolution). NHDPlus HR是一个全美整合的水文地理和搞成数据集，包括NHD径流网，WBD水文单元，流域，径流流向和flow accumulation rasters，以及 value-added attributes (VAAs)（包括降水，温度，径流等数据）。现在还在迭代开发阶段。

接下来分别记录下这三个数据集的情况。

### National Hydrography Dataset (NHD)

NHD表示了全美的水系网络，比如 rivers, streams, canals, lakes, ponds, coastline, dams, 和 streamgages.

目前的NHD版本数据，the NHD High Resolution，比例尺是1:24,000 scale or better (1:63,360 or better in Alaska)。该数据和WBD及3DEP数据一起共同用来构建the NHDPlus High Resolution.

可下载的地理数据库文件包括了NHD复杂数据库模型，包括multiple feature datasets, feature classes, event feature classes, attribute tables, relationship classes, domains, 以及 feature-level metadata.

可下载的shapefile通过将所有 feature classes 包含在不同的shapefiles和tables中简化了结构。

NHD文件地理数据库下载的数据在 Hydrography feature dataset中包括了NHD数据，在第二个feature dataset中还有WBD。

NHDFlowline是基本的径流网络，代表了空间几何，有属性，有stream/river and artificial path vector features以及定位features的线性参考measures。还有其他一些canal/ditch, pipeline, connector, underground conduit, and coastline等。NHDLine包含一些对与水系网络非核心的成分。

河湖水体由NHDWaterbody表示，比如 lake/pond features，还有 swamp/marsh, reservoir, playa, estuary, 和 ice mass等。NHDArea包含了 stream/river feature，表示较宽的河流的面积。

NHD Point features主要是一些水文地理相关的点features，比如径流站点。

NHD Events作为map features 和 linearly referenced events. 比如径流站点这一Point features就是通过 linear referencing with a network address 来展示的。Events包括：NHDPointEventFC, NHDLineEventFC, and NHDAreaEventFC ，分别代表点线面。

NHD Tables包括元数据等。

### Watershed Boundary Dataset

WBD数据应用非常多，是NHD数据的搭档，是 NHDPlus High Resolution (NHDPlus HR)数据集的组成部分。WBD是一个无缝的全美的hydrologic unit dataset。简单地说，hydrologic unit（HU）代表了汇流到河网的landscape的区域。更具体的讲，HU定义了汇流到出口断面的地表径流的流域。一个HU可以代表整个流域，也可以是代表一个部分的。WBD中的HU边界由topographic, hydrologic, and other relevant landscape characteristics without regard for administrative, political, or jurisdictional boundaries定义。 有六个必须的和两个可选的共8个层级。

HU组成了一个标准的用于表示全美水文信息的系统。每个HU都有唯一编码标识。2-12每多两位数字标识一个层级，14和16两种位数数字在部分地区有标识。

HU有Editing Tools，因为我也不会去编辑美国的这个数据，所以就不记录了。


关于hydrologic unit（HU）的更多介绍可以参考[Hydrologic Unit Maps](https://water.usgs.gov/GIS/huc.html)。以及官网的[数据模型](https://prd-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/WBDv2.21_poster_8_1_16fin.pdf)和[制作标准](https://pubs.usgs.gov/tm/11/a3/)。

### NHDPlus High Resolution

NHDPlus HR是一个全美的the flow of water across the landscape and through the stream network的地理空间模型。前面已经简单介绍了，它有1:24,000 scale，和1/3 arc-second (10 meter ground spacing) 3D高程数据，不但包含了 NHD and WBD ，还有一系列的[value-added attributes (VAAs)](https://www.usgs.gov/core-science-systems/ngp/national-hydrography/value-added-attributes-vaas)，流域特性数据，河流流向等各类数据。

它是在比较成功的NHDPlus Version 2之后建设的，比NHDPlus Version 2更加详细，不过现阶段还没完成。因此，现阶段可以更多地看看[NHDPlus Version 2](https://www.epa.gov/waterdata/nhdplus-national-hydrography-dataset-plus)数据。接下来简单记录下关于NHDPlus的情况。

National Hydrography Dataset Plus (NHDPlus) 是一个全美地表水地理空间框架。由U.S. EPA（Environmental Protection Agency） 和USGS共同开发和维护。

NHDPlus 是一系列地理空间产品，基于National Hydrography Dataset (NHD), the National Elevation Dataset (NED) （即前面有简要介绍的The National Map相关数据）和 the Watershed Boundary Dataset (WBD)构建。构建的动机是EPA为了估计径流volume和veocity以支持pollutant dilution (fate-and-transport) modeling 。

NHDPlus整合了NHD stream network 和 WBD hydrologic unit boundaries 以及 he NED gridded land surface 。这样水文条件下的地表可以为每个NHD径流段划分流域。NHDPlus catchments也用来将stream segments和其他landscape attributes，比如land cover，联系。

这些数据使得水文社区能开发大量水相关的应用。NHDPlus第一版于2006年发布，后面2012年发布了第二版。由于第二版相比第一版有很大提升，因此基本不用第一版了。

更多内容可以参考：[NHDPlus (National Hydrography Dataset Plus)](https://www.epa.gov/waterdata/learn-more)

## NH数据获取

 NHDPlus High Resolution (NHDPlus HR), National Hydrography Dataset (NHD), and Watershed Boundary Dataset (WBD) 均可下载。NHD数据下载后有包括WBD；NHDPlus HR 下载后则包括NHD和WBD。
 
 USGS已经将数据都传至云端了。现在的下载都是直接从云端下载的。
 
 数据可以直接通过[National Map Download viewer](https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View)下载，也可以通过[The National Map Download Manager](https://viewer.nationalmap.gov/apps/download_manager/)下载。
 
 也可以直接根据链接来下载。各链接可查看[官网](https://www.usgs.gov/core-science-systems/ngp/national-hydrography/access-national-hydrography-products)。
 
 个人认为使用python直接通过链接下载较好。相关代码后续补充。
 
  NHDPlus High Resolution (NHDPlus HR)数据仍在开发中，因此这里暂时用NHDPlus (National Hydrography Dataset Plus的获取为例子记录。主要参考：[Get NHDPlus (National Hydrography Dataset Plus) Data](https://www.epa.gov/waterdata/get-nhdplus-national-hydrography-dataset-plus-data) 。
  
  NHDPlus Version 2 (NHDPlusV2) Data 包括的内容有：
  
- 1:100K National Hydrography Dataset (NHD).
- 30 meter National Elevation Dataset (NED).
- Nationally complete Watershed Boundary Dataset (WBD).
- 用于径流网导航、分析和展示的属性值集
- An elevation-based catchment for each flowline in the stream network.
- Catchment characteristics.
- Headwater node areas.
- Cumulative drainage area characteristics.
- Flow direction, flow accumulation and elevation grids.
- Flowline min/max elevations and slopes.
- Flow volume & velocity estimates for each flowline in the stream network.
- Catchment attributes and network accumulated attributes.
- Various grids from the hydro-enforcement process including the hydro-enforced DEM.

数据是按照HUC02来分区组织的。下载可以直接在网站上下载，也可以编写python程序下载。

另外还有一个网站，[NHDPlus Version 2](http://www.horizon-systems.com/NHDPlus/NHDPlusV2_home.php)，也可以从该网站下载数据。根据[Hydrologic Unit Codes: HUC 4, HUC 8, and HUC 12](https://enviroatlas.epa.gov/enviroatlas/DataFactSheets/pdf/Supplemental/HUC.pdf)提示，下载页面是[National Data](http://www.horizon-systems.com/NHDPlus/V2NationalData.php)。

另外关于WBD流域数据的下载，还有一个网站可以下载一些处理好的数据：https://nrcs.app.box.com/v/gateway/folder/39640323180

这个资源的来源是：一份ppt[Data Sources for GIS in Water Resources](http://snr.unl.edu/kilic/giswr/2015/Water%20Resources%20Data.pptx)，这份ppt详细的总结了水资源中用到的GIS数据源，是一份很好的材料，建议自己收藏一份。

USGS有一个data catalog，可以查看：[ScienceBase Catalog](https://www.sciencebase.gov/catalog/item/4f4e4760e4b07f02db47df9c)，里面有很多数据内容。

关于数据的下载代码，暂时还没时间处理，后续再补充。目前如果需要数据下载处理，先手动处理好，然后再上传到kaggle等云端数据集库中，可方便后面使用。