# -*- coding=utf-8 -*-
# The files downloaded from "http://data.cma.cn/'(Chinese meteorology data website) should be handled for our intends
# First, if we have downloaded the files, we need to change the file names, because its suffix leads to a misunderstand for computers
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
        if num == -1:
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


if __name__ == "__main__":
    """Note: before you run this program, you'd better clear up your data_download_directory!!!"""
    print("Start:")
    data_download_directory = read_config.read_radar_data_dir('../config.ini', 'radar-data-config',
                                                              'data_download_directory')
    txt_directory = read_config.read_radar_data_dir('../config.ini', 'radar-data-config',
                                                    'data_txt_directory')
    wget_from_txt(txt_directory, data_download_directory)
    data_decompress_directory = read_config.read_radar_data_dir('../config.ini', 'radar-data-config',
                                                                'data_decompress_directory')
    decompress_download_data(data_download_directory, data_decompress_directory)
    print('END!')
