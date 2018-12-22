"""雨量站数据先从国电数据库中读取,需要对国电数据库里存储的降雨数据有比较清楚的认识,需要核对数据"""
import cx_Oracle
import pymysql
import read_config


def pixel_number_position(center_position_array, pixel_x_length, pixel_y_length):
    """Since we have done Guodian Project, data in Guodian Database should be utilized. The position of pixels in
    Guodian database need to be coordinated with the pixel we get from cma in order to utilize other codes,
    such as hydrology model, rain-gauge station position, etc. If the relationship of pixels in cma and guodian is
    one by one, we can store the value into database directly, else we should rescale the data. But the rescaling
    process is very troubling, so it is a better way to change data from database. """
    '''select data from t_bd_realtime as the rain-gauge data.'''
    lab_url = read_config.read_radar_data_dir('config.ini', 'lab-db', 'url')
    lab_username = read_config.read_radar_data_dir('config.ini', 'lab-db', 'username')
    lab_password = read_config.read_radar_data_dir('config.ini', 'lab-db', 'password')
    lab_database = read_config.read_radar_data_dir('config.ini', 'lab-db', 'database')
    select_rain_gauge_sql = "select * from t_bd_realtime where ENT_ID in " \
                            "(15,19,23,82,181,182,183,251,252,254,255,256,257,258,260,261,262,263,267,268,269,270,271,272,274,322,341,361,362)"
    all_rain_gauge_db_data = mysql_select(lab_url, lab_username, lab_password, lab_database, select_rain_gauge_sql)
    # SQL 插入语句,insert radar data to aliyun database
    url = read_config.read_radar_data_dir('config.ini', 'aliyun-db', 'url')
    username = read_config.read_radar_data_dir('config.ini', 'aliyun-db', 'username')
    password = read_config.read_radar_data_dir('config.ini', 'aliyun-db', 'password')
    database = read_config.read_radar_data_dir('config.ini', 'aliyun-db', 'database')
    insert_sql = "INSERT INTO t_bd_time_sequence " \
                 "(`id`, `ent_id`, `ent_name`, `proper_id`, `proper_name`, `time_step_unit`, `time`, `time_step_length`, `value`)" \
                 " VALUES (1, 1, 'test', 1, 'test', 'h', '2018-01-01 00:00:00', 1, 11);"
    mysql_insert(url, username, password, database, insert_sql)


def oracle_select():
    """connect to oracle database, and execute 'select'"""
    '''Note: Set the environment variable PATH to include the path that contains OCI.dll, if it is not already set, 
    and remeber restart your python IDE ! '''
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


def mysql_insert(url, username, password, database, sql):
    """connect to mysql database, and execute 'insert'"""
    db = pymysql.connect(url, username, password, database)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


def mysql_insert_batch(url, username, password, database, batchsql, param):
    """connect to mysql database, and execute 'insert' in batches"""
    db = pymysql.connect(url, username, password, database)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    '''批量插入数据,sql语句。要注意的是里面的参数，不管什么类型，统一使用%s作为占位符:insert into 表名(参数名1,参数名2) value(%s,%s)
    parameters: (('param1', 'param2'), ('param1', 'param2'))'''
    cursor.executemany(batchsql, param)
    # 关闭数据库连接
    db.close()


if __name__ == "__main__":
    url = read_config.read_radar_data_dir('config.ini', 'aliyun-db', 'url')
    username = read_config.read_radar_data_dir('config.ini', 'aliyun-db', 'username')
    password = read_config.read_radar_data_dir('config.ini', 'aliyun-db', 'password')
    database = read_config.read_radar_data_dir('config.ini', 'aliyun-db', 'database')
    insert_sql = "INSERT INTO t_bd_time_sequence " \
                 "(`id`, `ent_id`, `ent_name`, `proper_id`, `proper_name`, `time_step_unit`, `time`, `time_step_length`, `value`)" \
                 " VALUES (1, 1, 'test', 1, 'test', 'h', '2018-01-01 00:00:00', 1, 11);"
    mysql_insert(url, username, password, database, insert_sql)
