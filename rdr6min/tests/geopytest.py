import geopy
import geopy.distance


def get_distance_point(lat, lon, distance, direction):
    """
    根据经纬度，距离，方向获得一个地点
    :param lat: 纬度
    :param lon: 经度
    :param distance: 距离（千米）
    :param direction: 方向（北：0，东：90，南：180，西：270）
    :return:
    """
    start = geopy.Point(lat, lon)
    d = geopy.distance.VincentyDistance(kilometers=distance)
    return d.destination(point=start, bearing=direction)


p = get_distance_point(39.90733345, 116.391244079988, 8.5, 90)
print(p.latitude, p.longitude)

import numpy as np

a = np.array([0, 30, 45, 60, 90])
print('含有正弦值的数组：')
sin = np.sin(a * np.pi / 180)
print(sin)
print('\n')
print('计算角度的反正弦，返回值以弧度为单位：')
inv = np.arcsin(sin)
print(inv)
print('\n')
print('通过转化为角度制来检查结果：')
print(np.degrees(inv))
print('\n')
print('arccos 和 arctan 函数行为类似：')
cos = np.cos(a * np.pi / 180)
print(cos)
print('\n')
print('反余弦：')
inv = np.arccos(cos)
print(inv)
print('\n')
print('角度制单位：')
print(np.degrees(inv))
print('\n')
print('tan 函数：')
tan = np.tan(a * np.pi / 180)
print(tan)
print('\n')
print('反正切：')
inv = np.arctan(tan)
print(inv)
print('\n')
print('角度制单位：')
print(np.degrees(inv))


def calc_angle(x_point_s, y_point_s, x_point_e, y_point_e):
    angle = 0
    y_se = y_point_e - y_point_s
    x_se = x_point_e - x_point_s
    if x_se == 0 and y_se > 0:
        angle = 360
    if x_se == 0 and y_se < 0:
        angle = 180
    if y_se == 0 and x_se > 0:
        angle = 90
    if y_se == 0 and x_se < 0:
        angle = 270
    if x_se > 0 and y_se > 0:
        angle = np.atan(x_se / y_se) * 180 / np.pi
    elif x_se < 0 and y_se > 0:
        angle = 360 + np.atan(x_se / y_se) * 180 / np.pi
    elif x_se < 0 and y_se < 0:
        angle = 180 + np.atan(x_se / y_se) * 180 / np.pi
    elif x_se > 0 and y_se < 0:
        angle = 180 + np.atan(x_se / y_se) * 180 / np.pi
    return angle


print(calc_angle(256, 255, 250, 255))

vec1 = np.array([3,0])
vec2 = np.array([0,4])
distance = np.linalg.norm(vec1 - vec2)
print(distance)
