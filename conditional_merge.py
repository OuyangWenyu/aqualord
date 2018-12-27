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
import pandas as pd

import pyKriging
from pyKriging.krige import kriging
from pyKriging.samplingplan import samplingplan
from pykrige.ok import OrdinaryKriging
import pykrige.kriging_tools as kt
import numpy as np
from geopy.distance import vincenty
from pytime import pytime

import data_preprocess
import project_util
import matplotlib.pyplot as plt
import os

# TODO: 需要测试及代码重构，python应该多从矩阵的角度思考计算的方式
'''get discrete points by rain gauges from database'''
start_time = '2017-08-05 00:00:00'
end_time = '2017-08-10 00:00:00'
time_step_type = str(project_util.TimeUnitType.Hour.value)
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
radar_center_coordinate_x = project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_longitude')
radar_center_coordinate_y = project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_latitude')
radar_resolution_x = project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_resolution_x')
radar_resolution_y = project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_resolution_y')
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
gridx = np.arange(0, radar_center_coordinate_x * 2, 1)
gridy = np.arange(0, radar_center_coordinate_y * 2, 1)
'''krige the rain gauge observations'''
# Create the ordinary kriging object. Required inputs are the X-coordinates of
# the data points, the Y-coordinates of the data points, and the Z-values of the
# data points. If no variogram model is specified, defaults to a linear variogram
# model. If no variogram model parameters are specified, then the code automatically
# calculates the parameters by fitting the variogram model to the binned
# experimental semivariogram. The verbose kwarg controls code talk-back, and
# the enable_plotting kwarg controls the display of the semivariogram.
OK = OrdinaryKriging(x_in_radar_grid, y_in_radar_grid, z_rain_gauge_data, variogram_model='linear',
                     verbose=False, enable_plotting=True)
'''the enable-plotting controls the display of semivariogram, so we can check it to choose the best r(d) fitting 
curve '''
# Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
# grid of points, on a masked rectangular grid of points, or with arbitrary points.
# (See OrdinaryKriging.__doc__ for more information.)
z, ss = OK.execute('grid', gridx, gridy)
'''z is the result, and ss is the variance. So, next ,we can visualize the interpolation data'''
kt.write_asc_grid(gridx, gridy, z, filename="output.asc")

X, Y = np.meshgrid(gridx, gridy)

C = plt.contour(X, Y, z, 8, colors='black')  # 生成等值线图
plt.contourf(X, Y, z, 8)
plt.clabel(C, inline=1, fontsize=10)
plt.show()
'''get volume-integrated grid data by radar. We have many radar graphs, but we can't read them one-time, because the 
memory needed to load data is too big to be satisfied. For that reason, we need a loop and divide-and-conquer them 
one by one '''
rootdir = project_util.read_radar_data_dir('config.ini', 'radar-data', 'data_directory')
radar = project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_code')
files_list = os.listdir(rootdir)


def read_radar_data_in_positions(radar_data, x_in_radar_grid, y_in_radar_grid):
    """read radar data in position(x_in_radar_grid,y_in_radar_grid) —— use iloc """
    data_frame = pd.DataFrame(radar_data)
    return data_frame.iloc[x_in_radar_grid, y_in_radar_grid]


def write_radar_merge_data(precipitation, rain_date_time):
    """construct all datas and store in the table "t_bd_radar_precipitation". It would be better that zero values are
    not stored """
    url = project_util.read_radar_data_dir('config.ini', 'data-db', 'url')
    username = project_util.read_radar_data_dir('config.ini', 'data-db', 'username')
    password = project_util.read_radar_data_dir('config.ini', 'data-db', 'password')
    database = project_util.read_radar_data_dir('config.ini', 'data-db', 'database')
    table = "t_bd_radar_precipitation"
    params = []
    radar_center_x = int(project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_x'))
    radar_center_y = int(project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_y'))
    radar_radius_in_graph = int(project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_radius_in_graph'))
    radar_center = np.array([radar_center_x, radar_center_y])
    # sql = "select * from t_be_radar_grid"
    # radar_grids = utils.mysql_select(url, username, password, database, sql)
    count = 0
    for i in range(len(precipitation)):
        for j in range(len(precipitation[i])):
            xy_in_graph = np.array([i, j])
            if np.sqrt(np.sum(np.square(radar_center - xy_in_graph))) <= radar_radius_in_graph:
                # the area where the distance is shorter than the radius(250 grids)
                grid_id = count
                x_in_graph = i
                y_in_graph = j
                time = rain_date_time
                time_unit_type = 'h'
                time_unit_length = 1
                precipitation_value_min = str(precipitation[i][j][0])
                precipitation_value_max = str(precipitation[i][j][1])
                temp = (
                    grid_id, x_in_graph, y_in_graph, time, time_unit_type, time_unit_length, precipitation_value_min,
                    precipitation_value_max)
                count = count + 1
                if precipitation[i][j][1] > 0:
                    # we won't store 0, or the data in db will be too big.
                    params.append(temp)
    fields = ['grid_id', 'x_in_graph', 'y_in_graph', 'time', 'time_unit_type', 'time_unit_length',
              'precipitation_value_min', 'precipitation_value_max']
    project_util.mysql_insert_fields_batch(url, username, password, database, table, fields, params)


for i in range(0, len(files_list)):
    if files_list[i][-5:] == radar:
        file_list = os.listdir(rootdir + '/' + files_list[i])
        for j in range(len(file_list)):
            path = os.path.join(rootdir + '/' + files_list[i] + '/', file_list[i])
            radar_data = data_preprocess.read_radar_graph_data(path)
            '''krige radar data at the rain gauge locations'''
            # read radar data at the rain gauge locations
            radar_data_in_rain_gauge = read_radar_data_in_positions(radar_data, x_in_radar_grid, y_in_radar_grid)
            # krige
            ok_radar = OrdinaryKriging(x_in_radar_grid, y_in_radar_grid, radar_data_in_rain_gauge.values,
                                       variogram_model='linear',
                                       verbose=False, enable_plotting=True)
            z_radar, ss_radar = OK.execute('grid', gridx, gridy)
            kt.write_asc_grid(gridx, gridy, z_radar, filename="radar_output.asc")
            '''compute the deviation between the radar-observation and kriging-radar'''
            deviation = radar_data - z_radar
            '''apply deviation to kriging-rain-gauge'''
            merge_data = deviation + z
            '''write data to database'''
            rain_graph_time = path[:-4][-14:]
            rain_date = rain_graph_time[:8]
            rain_time = rain_graph_time[8:10] + ':' + rain_graph_time[10:12] + ':' + rain_graph_time[12:14]
            rain_date_time = pytime.parse(rain_date + ' ' + rain_time)
            write_radar_merge_data(merge_data, rain_date_time)
