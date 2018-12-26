# coding:utf-8
"""雨量站数据先从国电数据库中读取,需要对国电数据库里存储的降雨数据有比较清楚的认识,需要核对数据"""
import read_config
from project_util import mysql_select, mysql_insert_batch


def pixel_number_position(center_position_array, pixel_x_length, pixel_y_length):
    return


def read_rain_gauge_data():
    """read rain gauge data from database"""
    return


def read_radar_data():
    """read radar data from database"""
    return


def prepare_rain_gauge_data():
    """Since we have done Guodian Project, data in Guodian Database should be utilized. The position of pixels in
    Guodian database need to be coordinated with the pixel we get from cma in order to utilize other codes,
    such as hydrology model, rain-gauge station position, etc. If the relationship of pixels in cma and guodian is
    one by one, we can store the value into database directly, else we should rescale the data. But the rescaling
    process is very troubling, so it is a better way to change data from database. """
    # select data from t_bd_realtime as the rain-gauge data.
    lab_url = read_config.read_radar_data_dir('config.ini', 'lab-db', 'url')
    lab_username = read_config.read_radar_data_dir('config.ini', 'lab-db', 'username')
    lab_password = read_config.read_radar_data_dir('config.ini', 'lab-db', 'password')
    lab_database = read_config.read_radar_data_dir('config.ini', 'lab-db', 'database')
    select_rain_gauge_sql = "select * from t_bd_realtime where ENT_ID in " \
                            "(15, 19, 23, 82, 181, 182, 183, 251, 252, 254, 255, 256, 257, 258, 260, 261, 262, 263, 267, 268, 269, 270, 271, 272, 274, 322, 341, 361, 362)"
    all_rain_gauge_db_data = mysql_select(lab_url, lab_username, lab_password, lab_database, select_rain_gauge_sql)
    # insert radar data to your-data-db database for convenient in batches
    url = read_config.read_radar_data_dir('config.ini', 'data-db', 'url')
    username = read_config.read_radar_data_dir('config.ini', 'data-db', 'username')
    password = read_config.read_radar_data_dir('config.ini', 'data-db', 'password')
    database = read_config.read_radar_data_dir('config.ini', 'data-db', 'database')
    table = "t_bd_time_sequence"
    params = []
    for i in range(len(all_rain_gauge_db_data)):
        id = all_rain_gauge_db_data[i][0]
        ent_id = all_rain_gauge_db_data[i][6]
        ent_name = ''
        proper_id = all_rain_gauge_db_data[i][1]
        proper_name = '时段累计降雨量'
        time_step_unit = 'h'
        time = all_rain_gauge_db_data[i][2]
        time_step_length = 1
        value = all_rain_gauge_db_data[i][3]
        description = 'from lab database'
        temp = (
            id, ent_id, ent_name, proper_id, proper_name, time_step_unit, time, time_step_length, value, description)
        params.append(temp)
    mysql_insert_batch(url, username, password, database, table, params)


if __name__ == "__main__":
    print()
