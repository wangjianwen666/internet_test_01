
# TODO:配置文件/yaml的封装



import yaml

# 定义一个读取配置文件的函数
def read_yaml(file):
    """ 读取yaml """
    with open(file, mode="r", encoding="utf8") as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
        return conf

# 写入配置文件
def write_yaml(file,data):
    with open(file,mode="w",encoding="utf8") as f:
        yaml.dump(data,f)