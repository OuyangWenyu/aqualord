"""从下载的雷达图中读取像素,根据最左上角的像素的地理位置,雷达图的分辨率,计算使用的投影坐标系下的所有像素的地理位置,并且与已有的桓仁数据库中的编号对应上"""

import numpy as np
import os

from PIL import Image
import read_config


def read_rgb(raw_image):
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


def precipitation_from_pixel(pixel_grey_array):
    """Precipitation has a relationship with the color, so we can get precipitation data from the pixel's rgb value.
    0-10 mean the corresponding precipitation, and the other four numbers are 241, 243, 254, 255. So 0,241,243,254,
    255 correspond to 0 precipitation. Since the data given as a range not a number, it would be better using
    3 dimensional array with an interval represented by two number storing in the 3rd dimension for the return value"""
    switchDic = {1: [0.1, 5],
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
            if pixel_grey_array[x][y] in [0, 241, 243, 254]:
                temp = [0, 0]
                array[x][y] = temp
            else:
                array[x][y] = switchDic.get(pixel_grey_array[x][y])
    return array


def pixel_number_position():
    """Since we have done Guodian Project, data in Guodian Database should be utilized. The number of pixels in
    Guodian database need to be coordinated with the pixel we get from cma."""
    return


def read_precipitation_from_image(raw_image):
    """The integrated process in which we read precipitation value from images downloaded consists of read_rgb,
    precipitation _from_pixel and pixel_number_position, and then we can get a map with pixel's num from Guodian
    database serving as key, and precipitation value serving as value """
    read_rgb(raw_image)
    return


if __name__ == "__main__":
    rootdir = read_config.read_radar_data_dir('config.ini', 'radar-data', 'data_directory')
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
    if os.path.isfile(path):
        read_precipitation_from_image(path)
