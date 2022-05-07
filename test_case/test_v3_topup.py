
import unittest
import ddt
import json
from common import request_handler
from middleware.handler2 import HandLer

# 初始化logger
logger = HandLer.logger
# 获取表格
test_data = HandLer.excel.read_data("Sheet3")

# 使用ddt数据驱动
@ddt.ddt
class Test_uesrlogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """ 前置条件，充值前登录获取token """
        cls.token = HandLer().token

    # 把测试用例数据，放到ddt里面，循环取用例数据
    @ddt.data(*test_data)
    def test_userlogin(self,test_info):
        # 访问接口前，先获取excel中要替换的数据
        headers = test_info["headers"]
        if "#token#" in headers:
            headers = headers.replace("#token#",self.token)

        # 充值接口的访问
        data = test_info["data"]
        resp = request_handler.new_requests(
            url= HandLer().yaml["host"] + test_info["url"],
            method=test_info["method"],
            headers=json.loads(headers),
            json=json.loads(data)
        )

        # 使用for循环的方式进行断言
        new_tase_info = json.loads(test_info["expected"])
        try:
            for key,valus in new_tase_info.items():
                self.assertEqual(valus,resp[key])
            logger.info("测试用例通过")
        except AssertionError as a:
            logger.error("测试用例不通过{}".format(a))
            # 抛出异常
            raise a

