

import os

# 配置文件的路径
CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
print(CONFIG_PATH)
# 项目路径
ROOT_PATH = os.path.dirname(CONFIG_PATH)
# 测试用例路径
CASE_PATH = os.path.join(ROOT_PATH,"test_case")
# 测试报告路径
RESPONSE_PATH = os.path.join(ROOT_PATH,"response")
# 测试数据的路径
DATA_PATH = os.path.join(ROOT_PATH,"test_data")
# yaml 配置文件的路径
YAML_PATH = os.path.join(CONFIG_PATH,"config.yml")
# 日志的路径
LOG_PATH = os.path.join(ROOT_PATH,"logs")



