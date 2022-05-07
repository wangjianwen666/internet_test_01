
import unittest
import ddt
import json
from common import request_handler
from middleware.handler import HandLer

# 初始化logger
logger = HandLer.logger
# 获取表格
test_data = HandLer.excel.read_data("Sheet2")

# 使用ddt数据驱动
@ddt.ddt
class Test_uesrlogin(unittest.TestCase):
    # 把测试用例数据，放到ddt里面，循环取用例数据
    @ddt.data(*test_data)
    def test_userlogin(self,test_info):

        # 访问接口
        resp = request_handler.new_requests(
            url= HandLer.yaml["host"] + test_info["url"],
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
            # 抛出异常
            raise a





