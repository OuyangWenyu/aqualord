import cx_Oracle
import pymysql

import read_config


def oracle_select():
    """connect to oracle database, and execute 'select'"""
    '''Note: Set the environment variable PATH to include the path that contains OCI.dll. After that, remeber restart 
    your python IDE ! '''
    url = read_config.read_radar_data_dir('config.ini', 'guodian-db', 'url')
    username = read_config.read_radar_data_dir('config.ini', 'guodian-db', 'username')
    password = read_config.read_radar_data_dir('config.ini', 'guodian-db', 'password')
    conn = cx_Oracle.connect(username + '/' + password + '@' + url + ':1521/ORCL')
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    # 使用execute方法执行SQL语句
    sql = "select * from product_component_version"
    cursor.execute(sql)
    # 使用fetchone()方法获取一条数据
    # data=cursor.fetchone()
    # 获取所有数据
    all_data = cursor.fetchall()
    print(all_data)
    # 获取部分数据，8条
    # many_data=cursor.fetchmany(8)
    # write in another db in aliyun
    conn.close()


def mysql_select(url, username, password, database, sql):
    """connect to mysql database, and execute 'select'"""
    db = pymysql.connect(url, username, password, database)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行SQL语句
    cursor.execute(sql)
    # 使用fetchone()方法获取一条数据
    # data=cursor.fetchone()
    # 获取所有数据
    all_data = cursor.fetchall()
    # 获取部分数据，8条
    # many_data=cursor.fetchmany(8)
    # write in another db in aliyun
    db.close()
    return all_data


def mysql_insert_batch(url, username, password, database, table, params):
    """connect to mysql database, and execute 'insert' in batches"""
    conn = pymysql.connect(url, username, password, database)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = conn.cursor()
    '''批量插入数据,sql语句。要注意的是里面的参数，不管什么类型，统一使用%s作为占位符:insert into 表名(参数名1,参数名2) value(%s,%s) parameters: (('param1', 
    'param2'), ('param1', 'param2'))。注意批量添加数据，数据格式必须list[tuple(),tuple(),tuple()]  或者tuple(tuple(),tuple(),tuple()) '''
    params_str = ''
    params_length = len(params)
    if params_length > 0:
        param_length = len(params[0])
        for j in range(param_length):
            if j == param_length - 1:
                params_str = params_str + '%s'
            else:
                params_str = params_str + '%s,'
    try:
        insert_sql = 'insert into ' + table + ' values(' + params_str + ')'
        cur.executemany(insert_sql, params)
    except Exception as e:
        print(e)
        print("sql execute failed")
    else:
        print("sql execute success")
    conn.commit()
    cur.close()
    conn.close()


def mysql_insert_fields_batch(url, username, password, database, table, fields, params):
    """connect to mysql database, and execute 'insert' in batches with given fields"""
    conn = pymysql.connect(url, username, password, database)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = conn.cursor()
    '''批量插入数据,sql语句。要注意的是里面的参数，不管什么类型，统一使用%s作为占位符:insert into 表名(参数名1,参数名2) value(%s,%s) parameters: (('param1', 
    'param2'), ('param1', 'param2'))。注意批量添加数据，数据格式必须list[tuple(),tuple(),tuple()]  或者tuple(tuple(),tuple(),tuple()) '''
    params_str = ''
    params_length = len(params)
    fields_str = ''
    if params_length > 0:
        param_length = len(params[0])
        if len(fields) != param_length:
            raise RuntimeError("域的个数和参数个数不一致！请检查！")
        for j in range(param_length):
            if j == param_length - 1:
                params_str = params_str + '%s'
                fields_str = fields_str + fields[j]
            else:
                params_str = params_str + '%s,'
                fields_str = fields_str + fields[j] + ','
    try:
        insert_sql = 'insert into ' + table + '(' + fields_str + ')' + ' values(' + params_str + ')'
        cur.executemany(insert_sql, params)
    except Exception as e:
        print(e)
        print("sql execute failed")
    else:
        print("sql execute success")
    conn.commit()
    cur.close()
    conn.close()
