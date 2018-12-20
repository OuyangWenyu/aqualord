"""从下载的雷达图中读取像素,根据最左上角的像素的地理位置,雷达图的分辨率,计算使用的投影坐标系下的所有像素的地理位置,并且与已有的桓仁数据库中的编号对应上"""
import os

from PIL import Image
import read_config


def read_rgb(raw_image):
    """get RGB value of all pixels,storing in an array"""
    im = Image.open(raw_image)
    width = im.size[0]
    height = im.size[1]
    im = im.convert('RGB')
    array = []
    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            rgb = (r, g, b)
            array.append(rgb)
    print(array)
    return array


def precipitation_from_pixel():
    """Precipitation has a relationship with the color, so we can get precipitation data from the pixel's rgb
    value """
    return


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
    rootdir = read_config.read_radar_data_dir('config.ini','radar-data', 'data_directory')
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
    if os.path.isfile(path):
        read_precipitation_from_image(path)
