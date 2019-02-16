# coding: utf-8
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
from pykrige.ok import OrdinaryKriging
import pykrige.kriging_tools as kt
import numpy as np
from geopy.distance import vincenty
from pytime import pytime

import data_preprocess
import project_util
import matplotlib.pyplot as plt
import os


def read_rain_gauge_data(rain_gauge_sites_id, start_time, end_time, time_step_type, time_step_length):
    """get discrete points by rain gauges from database.
    Parameters
    ----------
    for example,
    start_time = '2017-08-05 00:00:00'
    end_time = '2017-08-10 00:00:00'
    time_step_type = str(project_util.TimeUnitType.Hour.value)
    time_step_length = 1
    rain_gauge_sites_id = [15, 19, 23, 82, 181, 182, 183, 251, 252, 254, 255, 256, 257, 258, 260, 261, 262, 263, 267,
                          268, 269, 270, 271, 272, 274, 322, 341, 361, 362]
    Returns
    -------
    rain_gauges_data as a dataframe
    """
    '''read all rain_gauge_sites data, and then use 'iloc'/'loc' to get the data we need '''
    url, username, password, database = project_util.time_sequence_table()
    sql = "select * from t_bd_time_sequence where attribute_id=114 and time_step_unit=\"" + time_step_type + "\" and time_step_length=" + str(
        time_step_length) + " and time >= \"" + start_time + "\" and time<\"" + end_time + "\" order by ent_id, time; "
    select_data_temp = project_util.mysql_select(url, username, password, database, sql)
    print(select_data_temp)
    z_rain_gauge_data = select_data_temp.loc[select_data_temp['ent_id'].isin(rain_gauge_sites_id)]
    print(z_rain_gauge_data)
    # transform data to the form of np.array, need zero to fill up the array
    periods_num = project_util.time_period_num(start_time, end_time, time_step_type, time_step_length)
    datelist = pd.date_range(start_time, freq='H', periods=periods_num)
    rain_gauges_data = pd.DataFrame(np.zeros((len(datelist), len(rain_gauge_sites_id))), index=datelist,
                                    columns=rain_gauge_sites_id)
    print(rain_gauges_data)
    for rain_temp in z_rain_gauge_data.iterrows():
        time_temp = rain_temp[1].values[6]
        ent_temp = rain_temp[1].values[1]
        value_temp = rain_temp[1].values[8]
        rain_gauges_data.loc[time_temp, ent_temp] = value_temp
    print(rain_gauges_data)
    return rain_gauges_data


def rain_gauge_site_num_in_radar_grid(rain_gauge_sites_id, radar_center_x, radar_center_y, radar_resolution_x,
                                      radar_resolution_y):
    '''After getting rain gauges' rainfall data(2 dimensional data), calculate the grid number in radar graph of rain gauge
     by its geological coordination Firstly, give out a virtual position. the center of radar station is (126.12, 41.59)
     # Parameters:
     ---------------
     rain_gauge_sites_id: all pluviometers' coordinations
     radar_center_x: radar-center's x number not coordination
     radar_center_y: radar-center's y number not coordination
     '''
    url, username, password, database = project_util.time_sequence_table()
    sql = "select * from t_be_entity where id in (" + str(rain_gauge_sites_id)[1:-1] + ") order by id; "
    coordinates = project_util.mysql_select(url, username, password, database, sql)
    lat_long_itudes = coordinates.iloc[:, [6, 5]].values
    print(lat_long_itudes)
    # Note: 函数参数都是纬度latitude在前，经度longitude在后。
    radar_center_coordinate_x = float(
        project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_longitude'))
    radar_center_coordinate_y = float(
        project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_latitude'))
    radar_center_coordinate = (radar_center_coordinate_y, radar_center_coordinate_x)
    x_distance_in_radar_grid = []
    y_distance_in_radar_grid = []
    for i in range(len(lat_long_itudes)):
        radar_center_coordinate_temp_x = (radar_center_coordinate[0], lat_long_itudes[i][1])
        radar_center_coordinate_temp_y = (lat_long_itudes[i][0], radar_center_coordinate[1])
        distance_x_temp = vincenty(radar_center_coordinate_temp_x, lat_long_itudes[i]).km
        distance_y_temp = vincenty(radar_center_coordinate_temp_y, lat_long_itudes[i]).km
        '''Radars in our country are all located in north and east of the earth,
        So it means that bigger y, smaller latitude; bigger x, bigger longitude'''
        if lat_long_itudes[i][0] < radar_center_coordinate_y:
            y_distance_in_radar_grid.append(distance_y_temp / radar_resolution_y)
        else:
            y_distance_in_radar_grid.append(-distance_y_temp / radar_resolution_y)
        if lat_long_itudes[i][1] < radar_center_coordinate_x:
            x_distance_in_radar_grid.append(-distance_x_temp / radar_resolution_x)
        else:
            x_distance_in_radar_grid.append(distance_x_temp / radar_resolution_x)
    x_in_radar_grid = radar_center_x + np.array(x_distance_in_radar_grid)
    y_in_radar_grid = radar_center_y + np.array(y_distance_in_radar_grid)
    x_in_radar_grid = np.rint(x_in_radar_grid)
    y_in_radar_grid = np.rint(y_in_radar_grid)
    return x_in_radar_grid.astype(np.int32), y_in_radar_grid.astype(np.int32)


def rain_ordinary_kriging(radar_center_x, radar_center_y, radar_radius_in_graph,
                          radar_resolution_x, radar_resolution_y,
                          x_measure, y_measure, z_measure_data):
    """rainfall ordinary kriging.
    Parameters
    ----------
    center_grid_num_x: in radar map, the num in x-axis of center
    center_grid_num_y: in radar map, the num in y-axis of center
    x_measure: the x num of the points we have measured
    y_measure: the y num of the points we have measured
    z_measure_data: z_keige=z_keige(x,y) is the measurement value at point (x,y)
    Returns
    ----------
    z_krige: ndarray, Z-values of all specified grid
    ss_krige: ndarray,  Variance at specified grid points or at the specified set of points
    """
    # show the range of interpolation
    # plus '1' for the open interval
    # the last parameter "1.0" means one grid is "1", the type has to be float, or it will cast error
    gridx = np.arange(radar_center_x - radar_radius_in_graph,
                      radar_center_x - radar_radius_in_graph + radar_radius_in_graph * 2 + 1, 1.0)
    gridy = np.arange(radar_center_y - radar_radius_in_graph,
                      radar_center_y - radar_radius_in_graph + radar_radius_in_graph * 2 + 1, 1.0)
    '''krige the rain gauge observations. Create the ordinary kriging object. Required inputs are the X-coordinates 
    of the data points, the Y-coordinates of the data points, and the Z-values of the data points. If no variogram 
    model is specified, defaults to a linear variogram model. If no variogram model parameters are specified, 
    then the code automatically calculates the parameters by fitting the variogram model to the binned experimental 
    semivariogram. The verbose kwarg controls code talk-back, and the enable_plotting kwarg controls the display of 
    the semivariogram. '''
    temp_zero = np.zeros(1)
    if (z_measure_data <= temp_zero).all():
        z_krige = np.zeros((len(gridx), len(gridy)))
        ss_krige = np.zeros((len(gridx), len(gridy)))
    else:
        OK = OrdinaryKriging(x_measure, y_measure, z_measure_data, variogram_model='linear',
                             verbose=False, enable_plotting=True)
        '''the enable-plotting controls the display of semivariogram, so we can check it to choose the best r(d) fitting 
            curve '''
        # Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
        # grid of points, on a masked rectangular grid of points, or with arbitrary points.
        # (See OrdinaryKriging.__doc__ for more information.)
        z_krige, ss_krige = OK.execute('grid', gridx, gridy)
        '''z_keige is the result, and ss_krige is the variance. So, next ,we can visualize the interpolation data'''
        kt.write_asc_grid(gridx, gridy, z_krige, filename="output.asc")
        X, Y = np.meshgrid(gridx, gridy)
        C = plt.contour(X, Y, z_krige, 8, colors='black')  # 生成等值线图
        plt.contourf(X, Y, z_krige, 8)
        plt.clabel(C, inline=1, fontsize=10)
        plt.show()
    return z_krige, ss_krige


def read_radar_data_in_positions(radar_data, x_in_radar_grid, y_in_radar_grid):
    """read radar data in position(x_in_radar_grid,y_in_radar_grid)
     the x,y axis shown as following:
     ---------------> x  (East)
     |
     |
     |
     |
     |
     V
     y (South)
     x means longitude, y means latitude
     then, average a 2-D numpy array to a 1-D array
     Return
     ----------
     z-values in (x,y) given
     """
    radar_array = np.zeros((len(x_in_radar_grid), 2))
    for i in range(len(x_in_radar_grid)):
        radar_array[i] = radar_data[x_in_radar_grid[i], y_in_radar_grid[i]]
    print(radar_array)
    radar_data_in_rain_gauge_sites = radar_array.sum(1) / 2
    print(radar_data_in_rain_gauge_sites)
    return radar_data_in_rain_gauge_sites


def write_radar_merge_data(precipitation, rain_date_time):
    """construct all datas and store in the table "t_bd_condition_merge". It would be better that zero values are
    not stored """
    url, username, password, database = project_util.time_sequence_table()
    table = "t_bd_condition_merge"
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
                precipitation_value = str(precipitation[i][j])
                temp = (
                    grid_id, x_in_graph, y_in_graph, time, time_unit_type, time_unit_length, precipitation_value)
                count = count + 1
                if precipitation[i][j] > 0:
                    # we won't store 0, or the data in db will be too big.
                    params.append(temp)
    fields = ['grid_id', 'x_in_graph', 'y_in_graph', 'time', 'time_unit_type', 'time_unit_length',
              'precipitation_value']
    project_util.mysql_insert_fields_batch(url, username, password, database, table, fields, params)


def radar_map_at_time(rootdir, radar, time):
    """read a radar map of the 'radar' at the 'time' from the director 'rootdir'. 6分钟一个，但是不是都从00点开始，会有漏掉的数据，所以循环需要注意，目前采用按小时的方式
    TODO: the radar time is UTC time, so we have to convert it to the Beijing time
    Return
    -------
    the path of the map we need
    """
    files_list = os.listdir(rootdir)
    for i in range(0, len(files_list)):
        print(files_list[i][-14:-6])
        date_time_right = pytime.parse(time)
        print(date_time_right)
        print(files_list[i][-5:])
        if files_list[i][-5:] == radar:
            date_temp = pytime.parse(files_list[i][-14:-6])
            if date_temp == date_time_right.date():
                file_list = os.listdir(rootdir + '/' + files_list[i])
                for j in range(len(file_list)):
                    print(file_list[j][-18:-4])
                    date_time_temp = project_util.parse_datetime(file_list[j][-18:-4])
                    print(date_time_temp.hour)
                    if date_time_right.hour == date_time_temp.hour:
                        path = os.path.join(rootdir + '/' + files_list[i] + '/', file_list[j])
                        print(path)
                        break
                break
    return path


def radar_rain_gauge_merge(start_time, end_time):
    """merge radar data with rain gauge"""

    time_step_type = str(project_util.TimeUnitType.Hour.value)
    time_step_length = 1
    rain_gauge_sites_id = [15, 19, 23, 82, 181, 182, 183, 251, 252, 254, 255, 256, 257, 258, 260, 261, 262, 263, 267,
                           268, 269, 270, 271, 272, 274, 322, 341, 361, 362]
    zs_rain_gauge = read_rain_gauge_data(rain_gauge_sites_id, start_time, end_time, time_step_type, time_step_length)
    print(zs_rain_gauge.values)
    print(zs_rain_gauge.values[0])
    # read rain_gauge_site_num_in_radar_grid
    radar_center_x = int(project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_x'))
    radar_center_y = int(project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_y'))
    radar_resolution_x = float(project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_resolution_x'))
    radar_resolution_y = float(project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_resolution_y'))
    x_in_radar_grid, y_in_radar_grid = rain_gauge_site_num_in_radar_grid(rain_gauge_sites_id, radar_center_x,
                                                                         radar_center_y, radar_resolution_x,
                                                                         radar_resolution_y)
    periods_num = project_util.time_period_num(start_time, end_time, time_step_type, time_step_length)
    datelist = pd.date_range(start_time, freq='H', periods=periods_num)
    rootdir = project_util.read_radar_data_dir('config.ini', 'radar-data', 'data_directory')
    radar = project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_code')
    for i in range(len(datelist)):
        radar_map_path = radar_map_at_time(rootdir, radar, datelist[i])
        '''get volume-integrated grid data by radar. We have many radar graphs, but we can't read them one-time, because the
            memory needed to load data is too big to be satisfied. For that reason, we need a loop and divide-and-conquer them
            one by one '''
        radar_data_interval = data_preprocess.read_precipitation_from_image(radar_map_path)
        '''krige radar data at the rain gauge locations'''
        # read radar data at the rain gauge locations. Because the data of radar has the form of interval, we name it "range"
        radar_data_in_rain_gauge_sites = read_radar_data_in_positions(radar_data_interval, x_in_radar_grid,
                                                                      y_in_radar_grid)
        # To krige, we have to convert the range to a number. Here, I choose the way to average the range
        radar_radius_in_graph = int(
            project_util.read_radar_data_dir('config.ini', 'radar-data', 'radar_radius_in_graph'))
        z_radar, ss_radar = rain_ordinary_kriging(radar_center_x, radar_center_y, radar_radius_in_graph,
                                                  radar_resolution_x, radar_resolution_y, x_in_radar_grid,
                                                  y_in_radar_grid, radar_data_in_rain_gauge_sites)
        '''compute the deviation between the radar-observation and kriging-radar'''
        # radar_data have to be sliced to adapt the size of kriging's range
        radar_data = radar_data_interval.sum(2) / 2
        x_start_index = radar_center_x - radar_radius_in_graph
        y_start_index = radar_center_y - radar_radius_in_graph
        x_end_index = int((radar_center_x - radar_radius_in_graph + radar_radius_in_graph * 2) + 1)
        y_end_index = int((radar_center_y - radar_radius_in_graph + radar_radius_in_graph * 2) + 1)
        deviation = radar_data[x_start_index:x_end_index, y_start_index:y_end_index] - z_radar
        '''apply deviation to kriging-rain-gauge'''
        z_rain_gauge, ss_rain_gauge = rain_ordinary_kriging(radar_center_x, radar_center_y, radar_radius_in_graph,
                                                            radar_resolution_x, radar_resolution_y, x_in_radar_grid,
                                                            y_in_radar_grid, zs_rain_gauge.values[i])
        merge_data = deviation + z_rain_gauge
        '''write data to database'''
        rain_graph_time = radar_map_path[:-4][-14:]
        rain_date = rain_graph_time[:8]
        rain_time = rain_graph_time[8:10] + ':' + rain_graph_time[10:12] + ':' + rain_graph_time[12:14]
        rain_date_time = pytime.parse(rain_date + ' ' + rain_time)
        # write_radar_merge_data(merge_data, rain_date_time)
        return merge_data, x_start_index, y_start_index, x_end_index, y_end_index


if __name__ == "__main__":
    start_time = '2016-08-30 00:00:00'
    end_time = '2016-09-09 00:00:00'
    radar_rain_gauge_merge(start_time, end_time)
