
import unittest
import ddt
import json
from decimal import Decimal
from common import request_handler
from middleware.handler2 import HandLer
from common.excel_handler import ExcelHandler

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

    def setUp(self) -> None:
        """ 充值前查询/初始化 数据库 """
        self.db = HandLer.db_class()
    def tearDown(self) -> None:
        """ 关闭数据库 """
        self.db.close()

    # 把测试用例数据，放到ddt里面，循环取用例数据
    @ddt.data(*test_data)
    def test_userlogin(self,test_info):
        # 访问接口前，先获取excel中要替换的数据
        # headers = test_info["headers"]
        # if "#token#" in headers:
        #     headers = headers.replace("#token#",self.token)

        # 访问接口前，先获取excel中要替换的数据，使用正泽表达式的方式替换，调用Handler 里封装好的正泽表达式的方法
        headers = test_info["headers"]
        headers = HandLer().replace_data(headers)

        # 请求接口（充值）前，查询数据库余额
        user_info = self.db.query(
            "SELECT b.current_amount FROM lcb_value_add_stock_db.resource a,lcb_value_add_stock_db.resource_account b WHERE a.id = b.resource_id AND a.id = '101' LIMIT 1;",
            one=True
        )
        # 充值前，查询数据库余额，用变量接收
        before_money = user_info["current_amount"]

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

        # 充值成功需要验证数据库。 继续断言
        # 充值之前的金额 + 充值的金额 = 充值之后的金额
        if resp["statusCode"] == 200:
            user_info = self.db.query(
                "SELECT b.current_amount FROM lcb_value_add_stock_db.resource a,lcb_value_add_stock_db.resource_account b WHERE a.id = b.resource_id AND a.id = '101' LIMIT 1;"
            )
            # 查询充值后的金额，用变量接收
            after_money = user_info["current_amount"]
            # 断言，充值前和充值后，金额是否正确
            # 使用导入的 Decimal 函数，进行下面的数据转换（处理浮点数类型数据）,先转换成字符串，在使用 Decimal 转换成 Decimal 数据格式
            self.assertTrue(before_money + Decimal(str(data["storeId"])) == after_money)
            # self.assertEqual(len(before_money) + 1,after_money)

