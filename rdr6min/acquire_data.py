# coding:utf-8
"""雨量站数据先从国电数据库中读取,需要对国电数据库里存储的降雨数据有比较清楚的认识,需要核对数据. and the radar data downloading from cma can be referred to
another project:WaterCrawler """
import project_util
from project_util import mysql_sql, mysql_insert_batch


def prepare_rain_gauge_data():
    """Since we have done Guodian Project, data in Guodian Database should be utilized. The position of pixels in
    Guodian database need to be coordinated with the pixel we get from cma in order to utilize other codes,
    such as hydrology model, rain-gauge station position, etc. If the relationship of pixels in cma and guodian is
    one by one, we can store the value into database directly, else we should rescale the data. But the rescaling
    process is very troubling, so it is a better way to change data from database. """
    # select data from t_bd_realtime as the rain-gauge data.
    lab_url = project_util.read_radar_data_dir('config.ini', 'lab-db', 'url')
    lab_username = project_util.read_radar_data_dir('config.ini', 'lab-db', 'username')
    lab_password = project_util.read_radar_data_dir('config.ini', 'lab-db', 'password')
    lab_database = project_util.read_radar_data_dir('config.ini', 'lab-db', 'database')
    select_rain_gauge_sql = "select * from t_bd_realtime where ENT_ID in " \
                            "(15, 19, 23, 82, 181, 182, 183, 251, 252, 254, 255, 256, 257, 258, 260, 261, 262, 263, 267, 268, 269, 270, 271, 272, 274, 322, 341, 361, 362)"
    all_rain_gauge_db_data = mysql_sql(lab_url, lab_username, lab_password, lab_database, select_rain_gauge_sql)
    # TODO: 修改了代码 mysql_select返回的是dataframe，需要重新测试
    # insert radar data to your-data-db database for convenient in batches
    url = project_util.read_radar_data_dir('config.ini', 'data-db', 'url')
    username = project_util.read_radar_data_dir('config.ini', 'data-db', 'username')
    password = project_util.read_radar_data_dir('config.ini', 'data-db', 'password')
    database = project_util.read_radar_data_dir('config.ini', 'data-db', 'database')
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


# -*- coding=utf-8 -*- The files downloaded from "http://data.cma.cn/'(Chinese meteorology data website) should be
# handled for our intends First, if we have downloaded the files, we need to change the file names, because its
# suffix leads to a misunderstand for computers
import os
import shutil
import subprocess

import com_decom_press
import read_config


def decompress_download_data(data_download_directory, data_decompress_directory):
    """The format of data downloaded from the website given by 'txt' files are a little strange with a suffix of
    'Expires=...', so we have to deal with it for an unzipable format, and do the unzip-action """
    file_names = os.listdir(data_download_directory)
    for temp in file_names:
        print(temp)
        # 找到最右边_Expires= or @Expires=的"_"or"@"的下标
        num = temp.rfind('Expires=') - 1
        # if 'Expires=' doesn't exist
        if num < 0:
            continue
        new_name = temp[:num]
        print(new_name)
        print(data_download_directory + '/' + temp)
        print(data_download_directory + '/' + new_name)
        if os.path.exists(data_download_directory + '/' + new_name):
            continue
        os.rename(data_download_directory + '/' + temp, data_download_directory + '/' + new_name)
    new_file_names = os.listdir(data_download_directory)
    # decompress all files and then move them to a directory.
    for temp in new_file_names:
        decompress_directory = com_decom_press.extract_tarbz2(data_download_directory + '/' + temp)
        if decompress_directory == None:
            continue
        if not os.path.exists(data_decompress_directory):
            os.makedirs(data_decompress_directory)
        # if there already are file decompressed, we should skip. this contains two situations.
        if os.path.exists(data_decompress_directory + '/' + temp) or os.path.exists(
                data_decompress_directory + '/' + temp[:temp.rfind('.tar.bz2')]):
            continue
        shutil.move(decompress_directory, data_decompress_directory)
    print("The radar graph has been decompressed!")


def wget_from_txt(txt_directory, outpath):
    """Download data from website provided by txt files. There are a list of web urls in a txt file,
    and we should get data we want by a command like 'wget -P THE_TARGET_DIRECTORY -i THE_FILE_LIST' """
    # TODO: It seems that we need a synchronized download, or we will execute the decompress program before we finished the download that will leads to a uncomplete progress
    files = os.listdir(txt_directory)
    for filelist in files:
        filelist = txt_directory + '/' + filelist
        try:
            '''If your os is windows, you should have to download a "wget" from 
            "http://gnuwin32.sourceforge.net/packages/wget.htm", and remeber that restart your IDE'''
            cmd = 'wget -P ' + outpath + ' -i ' + filelist
            print(cmd)
            os.popen(cmd)
            print('\nSucceed: download data from ' + filelist)
        except:
            print('\nFailed: download data from ' + filelist)


"""这是一个压缩和解压缩的工具类"""
# !/bin/python
#
# site: www.ahlinux.com
# 压缩文件夹为 .tar.bz2
import tarfile
import os


def extract_tarbz2(file_route):
    """解压一个.tar.bz2，file_route表示被解压文件的位置，返回解压的目标文件夹"""
    num = file_route.rfind('.tar.bz2')
    # if it is not a file with suffix '.tar.bz2', we have to stop, and return the file_route itself
    if num == -1:
        return file_route
        # target_directory is where I want to uncompress the files which is created with name same as the file we will decoompress
    target_derectory = file_route[0:num]
    if not os.path.exists(target_derectory):
        os.mkdir(target_derectory)
    archive = tarfile.open(file_route, 'r:bz2')
    archive.debug = 1  # Display the files beeing decompressed.
    for tarinfo in archive:
        archive.extract(tarinfo, target_derectory)
    archive.close()
    return target_derectory


# 压缩为.tar.bz2文件
# archive = tarfile.open('RADA_CHN_DOR_L3_MOCPUP_OHP.20150930-Z9240.tar.bz2', 'w:bz2')
# archive.debug = 1  # Display the files beeing compressed.
# archive.add(r'd:/myfiles')  # d:/myfiles contains the files to compress
# archive.close()

import configparser


def read_radar_data_dir(config_file_name, config_section_name, config_option_name):
    """根据配置文件的名称，配置section的名称和配置option的名称获取目标文件夹"""
    global target_directory
    cf = configparser.ConfigParser()
    # 读配置文件（ini、conf）返回结果是列表
    config_file = cf.read(config_file_name, encoding="utf-8")
    # 获取读到的所有sections(域)，返回列表类型
    config_sections = cf.sections()
    for config_section in config_sections:
        if config_section == config_section_name:
            # 某个域下的所有key，返回列表类型
            config_options = cf.options(config_section)
            for config_option in config_options:
                if config_option == config_option_name:
                    # 获取某个域下的key对应的value值
                    target_directory = cf.get(config_section, config_option)
                    break
            break
    return target_directory


if __name__ == "__main__":
    """Note: before you run this program, you'd better clear up your data_download_directory!!!"""
    print("Start:")
    data_download_directory = read_config.read_radar_data_dir('../config.ini', 'radar-data-config',
                                                              'data_download_directory')
    txt_directory = read_config.read_radar_data_dir('../config.ini', 'radar-data-config',
                                                    'data_txt_directory')
    # wget_from_txt(txt_directory, data_download_directory)
    data_decompress_directory = read_config.read_radar_data_dir('../config.ini', 'radar-data-config',
                                                                'data_decompress_directory')
    decompress_download_data(data_download_directory, data_decompress_directory)
    print('END!')
