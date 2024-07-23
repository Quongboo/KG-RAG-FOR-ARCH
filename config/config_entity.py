import yaml

def get_config():
    """
    获取配置文件
    :return:
    """
    with open('config/config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config
