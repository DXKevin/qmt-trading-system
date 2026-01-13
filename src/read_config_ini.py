import configparser

def read_config(config_file_path):
    """
    从 .ini 文件读取配置。

    Args:
        config_file_path (str): 配置文件的路径。

    Returns:
        dict: 包含所有配置项的字典。
    """
    config = configparser.ConfigParser()
    
    # 读取配置文件
    try:
        config.read(config_file_path, encoding='utf-8') # 指定编码，避免中文乱码
    except FileNotFoundError:
        print(f"错误：配置文件 {config_file_path} 未找到。")
        return {}
    except Exception as e:
        print(f"读取配置文件时发生错误: {e}")
        return {}

    # 将 ConfigParser 对象转换为普通字典
    config_dict = {}
    for section_name in config.sections():
        config_dict[section_name] = {}
        for key, value in config.items(section_name):
            config_dict[section_name][key] = value
    
    return config_dict

if __name__ == "__main__":
    config_path = 'config.ini'
    cfg = read_config(config_path)
    
    if cfg:
        print("数据库主机:", cfg['DATABASE']['host'])
        print("API密钥:", cfg['API']['api_key'])
        print("日志级别:", cfg['LOGGING']['level'])
    else:
        print("未能加载配置。")