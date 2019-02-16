'''流域内的雷达测雨数据和雨量站数据的融合'''
import project_util
from geojson_utils import point_in_multipolygon, json
import numpy as np
import conditional_merge


def calculate_average_precipitation(geojson_file, precipitation_data, x_start_index, y_start_index, x_end_index,
                                    y_end_index):
    """根据给定的各个像素的降雨数据计算面平均降雨"""
    average_precipitation = 0
    points = points_of_radar_map_in_basin(geojson_file)
    gridx = np.arange(x_start_index, x_end_index, 1.0)
    gridy = np.arange(y_start_index, y_end_index, 1.0)
    for i in gridx:
        for j in gridy:
            if [i, j] in points:
                average_precipitation = average_precipitation + precipitation_data[i - x_start_index, j - y_start_index]
    average_precipitation = average_precipitation / (len(gridx) * len(gridy))
    return average_precipitation


def points_of_radar_map_in_basin(geojson_file):
    """判断雷达图内哪些点在流域内，返回在流域内的像素格点的x_in_graph和y_in_graph"""
    sql = "select * from t_be_radar_grid"
    url, username, password, database = project_util.time_sequence_table()
    radar_grids = project_util.mysql_select(url, username, password, database, sql)
    print(radar_grids)
    radar_grid_in_basin = []
    for i in range(0, len(radar_grids)):
        center_longitude = radar_grids[i]['center_longitude']
        center_latitude = radar_grids[i]['center_latitude']
        if is_point_in_boundary(center_longitude, center_latitude, geojson_file):
            radar_grid_in_basin.append([radar_grids[i]['x_in_graph'], radar_grids[i]['y_in_graph']])
    return radar_grid_in_basin


def is_point_in_boundary(px, py, geojson_file):
    """给定一个点的经纬度坐标，判断是否在多多边形边界内"""
    json_file = open(geojson_file, encoding='utf-8')
    geojson_setting = json.load(json_file)
    print(geojson_setting)
    point_str = '{"type": "Point", "coordinates": [' + str(px) + ', ' + str(py) + ']}'
    print(point_str)
    # multipoly_str = '{"type":"MultiPolygon","coordinates":[[[[0,0],[0,10],[10,10],[10,0],[0,0]]],[[[10,10],[10,20],[20,20],[20,10],[10,10]]]]}'
    multipoly = geojson_setting['features'][1]['geometry']
    point = json.loads(point_str)

    return point_in_multipolygon(point, multipoly)
    # True


if __name__ == "__main__":
    start_time = '2016-08-30 00:00:00'
    end_time = '2016-09-09 00:00:00'
    merge_data, x_start_index, y_start_index, x_end_index, y_end_index = conditional_merge.radar_rain_gauge_merge(
        start_time, end_time)
    geojson_file = "tests/huanren_boundary_gc.json"
    average_rain = calculate_average_precipitation(geojson_file, merge_data, x_start_index, y_start_index, x_end_index,
                                                   y_end_index)
    print(average_rain)
