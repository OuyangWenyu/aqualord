"""The conditional merging process.
(a) The rainfall field is observed at discrete points by rain gauges.
(b) The rainfall field is also observed by radar on a regular, volume-integrated grid.
(c) Kriging of the rain gauge observations is used to obtain the best linear unbiased estimate of rainfall
    on the radar grid.
(d) The radar pixel values at the rain gauge locations are interpolated onto the radar grid using Kriging.
(e) At each grid point, the deviation C between the observed and interpolated radar value is computed.
(f) The field of deviations obtained from (e) is applied to the interpolated rainfall field obtained
    from Kriging the rain gauge observations.
(g) A rainfall field that follows the mean field of the rain gauge interpolation,
    while preserving the mean field deviations and the spatial structure of the radar field is obtained"""
import pyKriging
from pyKriging.krige import kriging
from pyKriging.samplingplan import samplingplan
from pykrige.ok import OrdinaryKriging
import numpy as np
from geopy.distance import vincenty
import project_util
import read_config
import time_unit_type

'''get discrete points by rain gauges from database'''
start_time = '2017-08-05 00:00:00'
end_time = '2017-08-10 00:00:00'
time_step_type = str(time_unit_type.TimeUnitType.Hour.value)
time_step_length = 1
rain_gauge_sites_id = [15, 19, 23, 82, 181, 182, 183, 251, 252, 254, 255, 256, 257, 258, 260, 261, 262, 263, 267, 268,
                       269, 270, 271, 272, 274, 322, 341, 361, 362]
z_rain_gauge_data = []
for i in len(rain_gauge_sites_id):
    z_rain_gauge_data.append(
        project_util.read_data_from_db_timesequence(rain_gauge_sites_id[i], 114, time_step_type, time_step_length,
                                                    start_time, end_time))
# transform data to the form of np.array, need zero to fill up the array
time_list = []
rain_gauge_data = []
rain_gauges_data = []
time_with_rain_list = []
time_length = project_util.time_period_num(start_time, end_time, time_step_type, time_step_length)
for i in range(len(z_rain_gauge_data)):
    time_with_rain_list_temp = []
    for j in range(len(z_rain_gauge_data[i])):
        time_with_rain_list_temp.append(z_rain_gauge_data[i][j][8])
    time_with_rain_list.append(time_with_rain_list_temp)

for i in range(len(rain_gauge_sites_id)):
    for j in range(time_length):
        time_temp = project_util.cal_end_time(start_time, time_step_type, i)
        time_list.append(time_temp)
        if time_temp not in time_with_rain_list:
            rain_gauge_data.append(0)
        else:
            rain_gauge_data.append(z_rain_gauge_data[i][9])
    rain_gauges_data.append(rain_gauge_data)
'''After getting rain gauges' rainfall data(2 dimensional data), calculate the grid number in radar graph of rain gauge
 by its geological coordination Firstly, give out a virtual position. the center of radar station is (126.12, 41.59)'''
coordinates = project_util.read_data_from_db_entity(rain_gauge_sites_id)
lat_long_itudes = []
for i in range(len(coordinates)):
    lat_long_itudes.append((coordinates[i][7], coordinates[i][6]))
# Note: 函数参数都是纬度latitude在前，经度longitude在后。
radar_center_coordinate_x = read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_longitude')
radar_center_coordinate_y = read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_latitude')
radar_resolution_x = read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_resolution_x')
radar_resolution_y = read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_resolution_y')
radar_center_coordinate = (radar_center_coordinate_y, radar_center_coordinate_x)
x_in_radar_grid = []
y_in_radar_grid = []
for i in range(len(lat_long_itudes)):
    radar_center_coordinate_temp_x = (radar_center_coordinate[0], lat_long_itudes[i][1])
    radar_center_coordinate_temp_y = (lat_long_itudes[i][0], radar_center_coordinate[1])
    distance_x_temp = vincenty(radar_center_coordinate_temp_x, lat_long_itudes[i]).miles
    distance_y_temp = vincenty(radar_center_coordinate_temp_y, lat_long_itudes[i]).miles
    x_in_radar_grid.append(distance_x_temp / radar_resolution_x)
    y_in_radar_grid.append(distance_y_temp / radar_resolution_y)

# show the range of interpolation
gridx = np.arange(0.0, radar_center_coordinate_x * 2, 0.5)
gridy = np.arange(0.0, radar_center_coordinate_y * 2, 0.5)
'''krige the rain gauge observations'''
# Create the ordinary kriging object. Required inputs are the X-coordinates of
# the data points, the Y-coordinates of the data points, and the Z-values of the
# data points. If no variogram model is specified, defaults to a linear variogram
# model. If no variogram model parameters are specified, then the code automatically
# calculates the parameters by fitting the variogram model to the binned
# experimental semivariogram. The verbose kwarg controls code talk-back, and
# the enable_plotting kwarg controls the display of the semivariogram.
OK = OrdinaryKriging(x_in_radar_grid, y_in_radar_grid, z_rain_gauge_data, variogram_model='linear',
                     verbose=False, enable_plotting=False)

# Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
# grid of points, on a masked rectangular grid of points, or with arbitrary points.
# (See OrdinaryKriging.__doc__ for more information.)
z, ss = OK.execute('grid', gridx, gridy)

# visualize the interpolation data

'''get volume-integrated grid data by radar from database'''

'''krige radar data at the rain gauge locations'''

'''compute the deviation between the radar-observation and kriging-radar'''

'''apply deviation to kriging-rain-gauge'''
