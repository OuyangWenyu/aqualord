# NLADS

目前主要使用的NLDAS数据是NLDAS-2: North American Land Data Assimilation System Forcing Fields，该数据集由NASA提供，数据集的时间范围是**1979/01/01到目前**，空间分辨率是八分之一度。关于数据本身的情况这里就不再赘述，主要记录下数据获取情况。参考：[NLDAS气象数据下载](https://mengfeimu.com/2019/03/11/NLDAS/)。

首先是linux或macos下的wget下载方法：

注意要先有EARTHDATA的账号。然后需要设置用户名和密码：

``` bash
cd ~ # 可以选择任意的目标文件夹
touch .netrc
echo "machine urs.earthdata.nasa.gov login uid_goes_here password password_goes_here" > .netrc
chmod 0600 .netrc
```

然后同一文件夹下，创建cookies文件：
```bash
touch .urs_cookies
```

单个文件下载：

```bash
wget --load-cookies ./.urs_cookies --save-cookies ./.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition http://hydro1.gesdisc.eosdis.nasa.gov/daac-bin/OTF/HTTP_services.cgi\?FILENAME\=%2Fdata%2FNLDAS%2FNLDAS_FORA0125_H.002%2F1982%2F001%2FNLDAS_FORA0125_H.A19820101.0100.002.grb\&FORMAT\=bmV0Q0RGLw\&BBOX\=38.204%2C-89.855%2C38.206%2C-89.853\&LABEL\=NLDAS_FORA0125_H.A19820101.0100.002.2019072152945.pss.nc\&SHORTNAME\=NLDAS_FORA0125_H\&SERVICE\=SUBSET_GRIB\&VERSION\=1.02\&LAYERS\=Eg\&DATASET_VERSION\=002
```

批量下载：

```bash
wget --load-cookies ./.urs_cookies --save-cookies ./.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition -i urls.txt
```

可以在命令后加上&放在后台运行，但由于每个文件都要和http通讯，很费时间，平均下载一天的数据文件（24个文件）需要下载40s，当然，可以考虑并行下载，会快点。

wget并行下载：

将以下内容存储为文件download_NLDAS.sh:

```bash
#!/bin/bash
infile="$1" # 这里的1是指执行该文件时添加的第一个参数
while IFS='' read -r url || [[ -n "$url" ]]; do
    wget --load-cookies ./.urs_cookies --save-cookies ./.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition $url &>/dev/null & 
done < "$1"
wait 
# &>/dev/nul 命令将滚动的输出隐去，设置为silient模式
# &：并行运算，将所有命令并行放在后台运行
```

直接执行download_NLDAS.sh下载的缺点是当文件数太多（上百上千），往往会报错，所以需要另外写个main.sh来调用download_NLDAS.sh，解决这种问题。由于是下载hourly的数据，因此每次调用download_NLDAS.sh来下载24个文件即一天的数据，如此循环：

```bash
#!/bin/bash
# main.sh
cd ~/Downloads/nldas
n=`cat urls.txt|wc -l`
# echo $n
for ((i=1; i<=$(($n/24)); i++));do
#for i in {1..$(($n/24))};do
	line1=$(($(($i*24))-23))
	line2=$(($i*24))
    # echo $line1
    # echo $line2
 	echo "$i of $(($n/24)) ..."
    sed -n "${line1},${line2}p" ./urls.txt > ./urls.temp.txt
    sh ./download_NLDAS.sh ./urls.temp.txt
done

if [ ! -d "./netcdfs" ]; then
    mkdir ./netcdfs
fi

mv ./*.nc ./netcdfs/

rm ./urls.temp.txt
```

接下来介绍下python下载的方式，参考[GES DISC 官方指导](https://disc.gsfc.nasa.gov/data-access#python)

首先安装pydap：

```bash
conda install -c conda-forge pydap
```

然后直接上代码：

``` python
# C:\mengfeimu\Data\2019_IECM\code\download_NLDAS.py
# jupyter notebook粘贴这些代码并不能运行（因为有并行的部分），需要存储为.py文件，然后在jupyter中运行 
# %run ./download_NLDAS.py

# 并行下载
import pandas as pd
import numpy as np
import datetime
from multiprocessing  import Pool, cpu_count

t1 = datetime.datetime.now()

def password_NLDAS():
    from pydap.cas.urs import setup_session
    username = 'mengfeimu'  # 使用自己的用户名和密码，这里仅仅是示例
    password = 'MMf1216069944'
    session = setup_session(username, password, ) # check_url=url
    return session

session = password_NLDAS()

def download_NLDAS2(param):
    url = param[0]
    y = param[1]
    m = param[2]
    d = param[3]
    h = param[4]
    r = session.request('Get',url)
    outfile = '{outdir}/{year}{month}{day}{hour}.nc'.format(outdir = outdir, \
                year = y, month = str(m).zfill(2), day = str(d).zfill(2), hour = str(h).zfill(2))
    with open(outfile, "wb") as code:
         code.write(r.content)

# latitude and longitude of the power plant 
# currently, just need to change lat and lon for another power plant
# change dates if study period is changed
lat  = 38.205
lon  = -89.854
lats = [lat-0.001, lat+0.001]
lons = [lon-0.001, lon + 0.001]

outdir = '../../2019_IECM/NLDAS2/55856_1982_2012'

dates = pd.date_range('19820101000000','20121231230000',freq='H')

# this url is obtained from NLDAS2 Simple Subst Wizard
# https://disc.gsfc.nasa.gov/datasets/NLDAS_FORA0125_H_V002/summary?keywords=NLDAS
url_1 = "http://hydro1.gesdisc.eosdis.nasa.gov/daac-bin/OTF/HTTP_services.cgi?FILENAME=%2Fdata%2FNLDAS%2FNLDAS_FORA0125_H.002%2F{year}%2F{doy}%2FNLDAS_FORA0125_H.A{year}{month}{day}.{hour}00.002.grb&FORMAT=bmV0Q0RGLw&BBOX={lat1}%2C{lon1}%2C{lat2}%2C{lon2}&LABEL=NLDAS_FORA0125_H.A{year}{month}{day}.{hour}00.002.2019072152945.pss.nc&SHORTNAME=NLDAS_FORA0125_H&SERVICE=SUBSET_GRIB&VERSION=1.02&LAYERS=Eg&DATASET_VERSION=002"

urls = []
params = []
for date in dates:  
    y = date.year
    m = date.month
    d = date.day
    h = date.hour

    doy = date.strftime('%j')

    url  = url_1.format(year = y, doy=str(doy).zfill(3),month = str(m).zfill(2), \
                   day = str(d).zfill(2), hour = str(h).zfill(2),\
                  lat1 = lats[0], lat2 = lats[1], lon1 = lons[0], lon2 = lons[1])
	urls.append(url)
    params.append([url,y,m,d,h])
# 输出urls到urls.txt:
# df_url = pd.DataFrame(data={'url':urls},index=dates)
# df_url.url.to_csv(path = '../../2019_IECM/NLDAS2/55856_1982_2012/urls.txt',\
                 index = False)
if __name__ == '__main__':
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    cores = cpu_count()  # leave one core idle cpu_count()-1
    p = Pool(processes = cores, maxtasksperchild = 4)
    
    p.map(download_NLDAS2, params)

    t2 = datetime.datetime.now()
    print("time:",format(t2-t1))
```