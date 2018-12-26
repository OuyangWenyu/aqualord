# coding:utf-8
"""从下载的雷达图中读取像素,根据最左上角的像素的地理位置,雷达图的分辨率,计算使用的投影坐标系下的所有像素的地理位置,并且与已有的桓仁数据库中的编号对应上"""

import numpy as np
import os

from PIL import Image

import project_util
import read_config
from pytime import pytime


def read_grey(raw_image):
    """get RGB value of all pixels,storing in an numpy array. Actually, because there are only 15 colors in a radar map,
    and their grey values are all different, different colors can be represented by their grey values instead of RGB."""
    im = Image.open(raw_image)
    width = im.size[0]
    height = im.size[1]
    array = np.zeros((width, height))
    for x in range(width):
        temp = np.zeros(height)
        for y in range(height):
            # the first parameter of 'getpixel' means width, the other one means height
            temp[y] = im.getpixel((x, y))
        array[x] = temp
    print(len(array))
    print(array)
    return array


def read_rgb(raw_image):
    """For PNG graph, we should recogonize rgb value"""
    im = Image.open(raw_image)
    pix = im.load()  # 导入像素
    width = im.size[0]
    height = im.size[1]
    array = np.zeros((width, height, 3))
    for x in range(width):
        temp = np.zeros((height, 3))
        for y in range(height):
            # the first parameter of 'getpixel' means width, the other one means height
            r, g, b = pix[x, y]
            temp[y] = [r, g, b]
        array[x] = temp
    return array


def precipitation_from_grey_pixel(pixel_grey_array):
    """Precipitation has a relationship with the color, so we can get precipitation data from the pixel's rgb value.
    1-10 mean the corresponding precipitation, and the other four numbers 241,243,254,255 correspond to [0,0]
    precipitation. Since the data given as a range not a number, it would be better to use 3 dimensional array with
    an interval represented by two number storing in the 3rd dimension for the return value """
    switch_dic = {1: [0.1, 5],
                  2: [5, 10],
                  3: [10, 25],
                  4: [25, 38],
                  5: [38, 50],
                  6: [50, 63],
                  7: [63, 75],
                  8: [75, 100],
                  9: [100, 125],
                  10: [125, 10000]
                  }
    width = len(pixel_grey_array)
    height = len(pixel_grey_array[0])
    array = np.zeros((width, height, 2))
    for x in range(width):
        for y in range(height):
            if pixel_grey_array[x][y] not in switch_dic.keys():
                temp = [0, 0]
                array[x][y] = temp
            else:
                array[x][y] = switch_dic.get(pixel_grey_array[x][y])
    print(array)
    '''Here, we get an array with precipitation values, but a phenomenon we don't expect still exists that some 
    pixels with precipitation values may be shadowed by the ones with values in [241,243] which represent some 
    geological or administrative concepts, so we have to use a window filter to revise this pixels. And how can we 
    get a suitable filter? search on the Internet...'''
    # TODO: Question: in the context of radar signal, change 241/243 to 0 or else?
    # Simple method: choose a fixed-size convolution kernel, a fixed-size stride, and then in the context of radar
    # signal, move the window. When the number of pixels with number larger than 0 is more than ones equal to 0,
    # assign the mode of numbers larger than 0 to the pixel with value 241/243.
    return array


def precipitation_from_pixel(pixel_rgb_array):
    """get legend's rgb from the following pixels:[527,485],[527,469],[527,453],[527,437],[527,421],[527,405],[527,
    390],[527,373],[527,357],[527,341]; their corresponding rgb values are [0,0,246],[1,160,33],[0,236,236],[255,255,
    0],[255,144,0],[255,0,0], [214,0,0], [192,0,0],[255,0,240],[173,144,240] """
    switch_dic = {(0, 0, 246): [0.1, 5],
                  (1, 160, 33): [5, 10],
                  (0, 236, 236): [10, 25],
                  (255, 255, 0): [25, 38],
                  (255, 144, 0): [38, 50],
                  (255, 0, 0): [50, 63],
                  (214, 0, 0): [63, 75],
                  (192, 0, 0): [75, 100],
                  (255, 0, 240): [100, 125],
                  (173, 144, 240): [125, 10000]
                  }
    width = len(pixel_rgb_array)
    height = len(pixel_rgb_array[0])
    array = np.zeros((width, height, 2))
    for x in range(width):
        for y in range(height):
            if tuple(pixel_rgb_array[x][y]) not in switch_dic.keys():
                array[x][y] = [0, 0]
            else:
                array[x][y] = switch_dic.get(tuple(pixel_rgb_array[x][y]))
    print(array)
    return array


def read_precipitation_from_image(raw_image, radar_date_time):
    """The integrated process in which we read precipitation value from images downloaded consists of read_rgb,
    precipitation _from_pixel and pixel_number_position, and then we can get a map with pixel's num from Guodian
    database serving as key, and precipitation value serving as value """
    '''if the image's format is .GIF, then it can be recoginized by its grey value only. However, if the format id 
    PNG, wo have to utilize RGB value '''
    precipitation_raw = []
    if raw_image[-3:] == 'GIF':
        grey_value = read_grey(raw_image)
        precipitation_raw = precipitation_from_grey_pixel(grey_value)
    else:
        grey_value = read_rgb(raw_image)
        precipitation_raw = precipitation_from_pixel(grey_value)
    '''After geting data from radar graph, we'd better store the data to database. However, because now I don't know 
    the correct longitude and latitude of radar grids,  what I can store are only the number of grid and 
    corresponding value. The data also stored in the table 't_bd_radar_precipitation' '''
    # Only first time, we have to construct all grids and store in the table "t_be_gird"
    # prepare_radar_grid(precipitation_raw)
    # Then, store the data in the table "t_bd_radar_precipitation"
    prepare_radar_rain_precipitation(precipitation_raw, radar_date_time)


def prepare_radar_grid(precipitation_raw):
    """construct all grids and store in the table "t_be_radar_gird"
    1小时累计降水产品采用的是每个 体扫描结束后的小时累计方式，即对对每一个2公里*1度的样本库降水率在每个体扫描结束后进行时间累计，
    得到一小时降水量，并在每个体扫结束后输出，生成该产品至少需要54分钟连续的体扫描资料（体扫瞄间隔不超过30分钟）。"""
    url = read_config.read_radar_data_dir('config.ini', 'data-db', 'url')
    username = read_config.read_radar_data_dir('config.ini', 'data-db', 'username')
    password = read_config.read_radar_data_dir('config.ini', 'data-db', 'password')
    database = read_config.read_radar_data_dir('config.ini', 'data-db', 'database')
    table = "t_be_radar_grid"
    params = []
    '''use polar coordinate system, the geological position of the center of radar station is (126.12, 41.59) and the
    resolution is 1 km * 1 degree. The range of radar is the area where the distance is shorter than the radius(250 grids)'''
    radar_center_x = int(read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_x'))
    radar_center_y = int(read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_y'))
    radar_radius_in_graph = int(read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_radius_in_graph'))
    radar_center = np.array([radar_center_x, radar_center_y])
    count = 0
    for i in range(len(precipitation_raw)):
        for j in range(len(precipitation_raw[i])):
            id = count
            radar_name = read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_name')
            x_in_graph = i
            y_in_graph = j
            center_longitude = 0
            center_latitude = 0
            height = 0
            width = 0
            project_coordinate_system = 'unknown'
            geology_coordinate_system = 'WGS-1984'
            resolution = '1km*1degree'
            nt = '0 means unknown'
            temp = (
                id, radar_name, x_in_graph, y_in_graph, center_longitude, center_latitude, height, width,
                project_coordinate_system, geology_coordinate_system,
                resolution, nt)
            xy_in_graph = np.array([x_in_graph, y_in_graph])
            print(np.sqrt(np.sum(np.square(radar_center - xy_in_graph))))
            if np.sqrt(np.sum(np.square(radar_center - xy_in_graph))) <= radar_radius_in_graph:
                # the area where the distance is shorter than the radius(250 grids)
                params.append(temp)
                count = count + 1
    project_util.mysql_insert_batch(url, username, password, database, table, params)


def prepare_radar_rain_precipitation(precipitation_raw, radar_date_time):
    """construct all datas and store in the table "t_bd_radar_precipitation". It would be better that zero values are
    not stored """
    url = read_config.read_radar_data_dir('config.ini', 'data-db', 'url')
    username = read_config.read_radar_data_dir('config.ini', 'data-db', 'username')
    password = read_config.read_radar_data_dir('config.ini', 'data-db', 'password')
    database = read_config.read_radar_data_dir('config.ini', 'data-db', 'database')
    table = "t_bd_radar_precipitation"
    params = []
    radar_center_x = int(read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_x'))
    radar_center_y = int(read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_center_y'))
    radar_radius_in_graph = int(read_config.read_radar_data_dir('config.ini', 'radar-data', 'radar_radius_in_graph'))
    radar_center = np.array([radar_center_x, radar_center_y])
    # sql = "select * from t_be_radar_grid"
    # radar_grids = utils.mysql_select(url, username, password, database, sql)
    count = 0
    for i in range(len(precipitation_raw)):
        for j in range(len(precipitation_raw[i])):
            xy_in_graph = np.array([i, j])
            if np.sqrt(np.sum(np.square(radar_center - xy_in_graph))) <= radar_radius_in_graph:
                # the area where the distance is shorter than the radius(250 grids)
                grid_id = count
                x_in_graph = i
                y_in_graph = j
                time = radar_date_time
                time_unit_type = 'h'
                time_unit_length = 1
                precipitation_value_min = str(precipitation_raw[i][j][0])
                precipitation_value_max = str(precipitation_raw[i][j][1])
                temp = (
                    grid_id, x_in_graph, y_in_graph, time, time_unit_type, time_unit_length, precipitation_value_min,
                    precipitation_value_max)
                count = count + 1
                if precipitation_raw[i][j][1] > 0:
                    # we won't store 0, or the data in db will be too big.
                    params.append(temp)
    fields = ['grid_id', 'x_in_graph', 'y_in_graph', 'time', 'time_unit_type', 'time_unit_length',
              'precipitation_value_min', 'precipitation_value_max']
    project_util.mysql_insert_fields_batch(url, username, password, database, table, fields, params)


def write_radar_graph_data_to_db():
    """get the precipitation interval from radar graph and insert them into database. Because the directory has two
    layers, a circle is a need """
    rootdir = read_config.read_radar_data_dir('config.ini', 'radar-data', 'data_directory')
    files_list = os.listdir(rootdir)
    for i in range(0, len(files_list)):
        if files_list[i][-5:] == 'Z9439':
            file_list = os.listdir(rootdir + '/' + files_list[i])
            for j in range(len(file_list)):
                path = os.path.join(rootdir + '/' + files_list[i] + '/', file_list[i])
                if os.path.isfile(path):
                    radar_graph_time = file_list[i][:-4][-14:]
                    radar_date = radar_graph_time[:8]
                    radar_time = radar_graph_time[8:10] + ':' + radar_graph_time[10:12] + ':' + radar_graph_time[12:14]
                    radar_date_time = pytime.parse(radar_date + ' ' + radar_time)
                    read_precipitation_from_image(path, radar_date_time)


if __name__ == "__main__":
    write_radar_graph_data_to_db()
