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
