# rainfall-estimation

#### 项目介绍
联合使用雷达降雨数据和雨量站降雨数据以期能够提升流域水文预报性能

#### 软件架构
项目文件组织结构（实时更新）：

                              | .gitignore
                              | conditional_merge.py
                              | config.ini
                              | data_from_db.py
    hydro-radar-precipitation | data_from_graph.py  
                              | project_util.py              
                              | read_config.py
                              | README.md
                              | time_unit_type.py


#### 使用说明
使用该项目程序目前需要**手动**构建项目忽略的文件夹及文件，包括以下内容：
1. data文件夹，其中存放测试需要的数据
2. tests文件夹，其中存放测试所使用的代码
3. config.ini文件，其结构形式如下：
```
[radar-data]
data_directory = YOUR_RADAR_GRAPH_DIRECTORY
[data-db]
url = YOUR_DATABASE_URL
username = YOUR_DATABASE_USERNAME
password = YOUR_DATABASE_PASSWORD
database = YOUR_DATABASE
```

#### 参与贡献

1. Fork 本项目
2. 新建 hydar_xxx 分支 (xxx可以是您的名称ID)
3. 提交代码
4. 新建 Pull Request