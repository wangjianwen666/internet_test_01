
import unittest
import ddt
import os
import json
from setting import config
from common.logging_handler import test_cases_logging
from common import excel_handler,request_handler,yaml_handler


# 导入yaml封装，通过该封装读取yaml 数据
yaml_data = yaml_handler.read_yaml(config.YAML_PATH)
# 然后取yaml 里的excel 配置
case_file = yaml_data["excel"]["file"]

# 初始化logger
logger_config = yaml_data["logger"]
logger = test_cases_logging(
    name=logger_config["name"],
    file=os.path.join(config.LOG_PATH,logger_config["file"]),
    root_level=logger_config["logger_level"],
    starm_level=logger_config["stream_level"],
    file_level=logger_config["file_level"]
)

# 获取excel测试数据
excel_file = os.path.join(config.DATA_PATH,case_file)
# 获取表格
test_data = excel_handler.ExcelHandler(excel_file).read_data("Sheet1")
logger.info("正在读取测试用例数据")


# 使用ddt数据驱动
@ddt.ddt
class Test_uesrlogin(unittest.TestCase):
    # 把测试用例数据，放到ddt里面，循环取用例数据
    @ddt.data(*test_data)
    def test_userlogin(self,test_info):

        # 访问接口
        resp = request_handler.new_requests(
            url= test_info["url"],
            method=test_info["method"],
            headers=json.loads(test_info["headers"]),
            json=json.loads(test_info["data"])
        )
        # 进行断言
        # self.assertEqual(
        #     json.loads(test_info["expected"])["statusCode"],
        #     resp["statusCode"]
        # )
        # self.assertTrue(
        #     json.loads(test_info["expected"])["msg"] == resp["msg"]
        # )

        # 使用for循环的方式进行断言
        new_tase_info = eval(test_info["expected"])
        try:
            for key,valus in new_tase_info.items():
                self.assertEqual(valus,resp[key])
            logger.info("测试用例通过")
        except AssertionError as a:
            logger.error("测试用例不通过{}".format(a))
            raise a





