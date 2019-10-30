import pandas as pd
import numpy as np
import xarray
from pytime import pytime

datelist = pd.date_range('2020/11/21 01:00:00', freq='H', periods=5)
print(datelist)
df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],
                  index=['cobra', 'viper', 'sidewinder'],
                  columns=['max_speed', 'shield'])
print(df)
print(df.loc[df['shield'].isin([6, 7, 8])])

data = {
    'date': datelist,
    'gender': [0, 1, 2, 3, 4],
    'height': np.random.randint(40, 50, size=5),
    'weight': np.random.randint(150, 180, size=5)
}
a = pd.DataFrame(data)
a.loc[a['date'].isin(['2020/11/21 01:00:00', '2020/11/21 02:00:00']), 'gender'] = [10, 11]
print(a)

column_lsit = [1, 2, 3, 4, 5, 6]
print(str(column_lsit)[1:-1])
df1 = pd.DataFrame(np.random.randn(len(datelist), len(column_lsit)), index=datelist, columns=column_lsit)
print(len(df1))

print(df1.iloc[:, [5, 4]])
#
# for row in a.iterrows():
#     temp = row[1].values[0]
#     print(temp)
#     df1.loc[temp, 2] = 10000
#     print(df1)
temp = pytime.parse("2018-05-05 00:00:00")
date_temp = pytime.parse("2018-05-05")
print(temp)
print(temp.date())
print(date_temp)
print(temp.date() == date_temp)

data = np.random.rand(4, 2, 2)
print(data)
print(data.sum(2))
# p = pd.Panel(data)
# print(p.values)
# print(p.iloc[[0, 1], [0, 1]].values)

# arr = xarray.DataArray(np.random.RandomState(0).randn(3, 3, 2),
#                        [(['a', 'b', 'c']), ([10, 20, 30]), ([1, 2])])
# print(arr)
# arr1 = arr.sum(dim='dim_2') / 2
# print(arr1)
#
# array = xarray.DataArray(np.random.randn(3, 3),
#                      coords=[(['a', 'b','c']), ([0, 1, 2])])
# print(array)
# stacked = array.stack(z=('dim_0', 'dim_1'))
# print(stacked)


x = [1, -2, 3, -4, 5]
y = [1, 2, 3, 4, 5]
a = 1.0002
b = a + np.array(x)
print(b)
b = np.rint(b)
print(b)
print(b.astype(np.int32))

c = np.zeros(1)
if (y > c).all():
    print(x > c)

e = np.random.rand(3, 4)
print(e)
print(e[1:2, 3:])

radar_grid_in_basin = []
df = pd.DataFrame([[1, 2], [4, 5], [7, 8]], columns=['max_speed', 'shield'])
print(df)
radar_grid_in_basin.append([df.loc[0, 'max_speed'], df.loc[1, 'shield']])
radar_grid_in_basin.append([df.loc[0, 'max_speed'], df.loc[1, 'shield']])
print(radar_grid_in_basin)

arrs = [[2, 15, 48, 4, 5], [6, 7, 6, 4, 1], [2, 3, 6, 6, 7], [4, 6, 8, 11, 2]]
arr_str = []
f = open('testARRS.txt', 'w+')
for i in range(len(arrs)):
    joints_frame = arrs[i]  # 每行
    arr_str.append(joints_frame)
    for j in range(len(joints_frame)):
        strNum = str(joints_frame[j])
        f.write(strNum)
        f.write(' ')
    f.write('\n')
f.close()
