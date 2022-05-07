
import os
import json
from jsonpath import jsonpath
from pymysql.cursors import DictCursor
from setting import config
from common import yaml_handler,excel_handler,logging_handler,request_handler
from common.mysql_handler import MysqlHandler


class MysqlHandlerMid(MysqlHandler):
    """ 读取配置文件选项，继承公共文件中的 mysqlhandler 的封装 """
    def __init__(self):
        """ 初始化所有的配置项，从yaml 中读取 """
        db_config = HandLer.yaml["db"]

        # 使用super（） 函数
        super(MysqlHandlerMid,self).__init__(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            passwd=db_config["password"],
            charset=db_config["charset"],
            cursorclass=DictCursor
        )



class HandLer:
    """ 初始化所有的数据，
    在其他模块当中重复使用
    是从 common 当中实例化对象
    """

    # 加载Python配置项
    conf = config

    # YAML 数据
    yaml = yaml_handler.read_yaml(os.path.join(config.YAML_PATH))       # 这里可以不用os.path.join,因为我ligin配置文件里已经配了具体文件

    # excel 数据
    # TODO: 变量名前加 双下划线，表示私有属性，只能内部调用，出了这个类或者函数，则不能调用
    __excel_path = conf.DATA_PATH
    __excel_file = yaml["excel"]["file"]
    excel = excel_handler.ExcelHandler(os.path.join(__excel_path,__excel_file))

    # logger 日志
    __logger_config = yaml["logger"]
    logger = logging_handler.test_cases_logging(
        name=__logger_config["name"],
        file=os.path.join(config.LOG_PATH, __logger_config["file"]),
        root_level=__logger_config["logger_level"],
        starm_level=__logger_config["stream_level"],
        file_level=__logger_config["file_level"],
    )

    # 把 MysqlHandlerMid 的类，导入到 Handler 类里面，方便调用
    db_class = MysqlHandlerMid


    @property
    def token(self):
        """ 把登录接口放到 handel里面.   使用 @property 把方法/函数 变成属性，方便调用。"""
        # 普通用户登录，获取token
        return self.login(self.yaml["user"])["token"]


    def login(self,user):
        """ 登录测试账号 """
        res = request_handler.new_requests(
            url=HandLer.yaml["host"] + "manage/common/api/user/smsLogin",
            method="post",
            headers={"appCode":"1011"},
            json=user,
        )
        # 提取token
        token = jsonpath(res,"$..token")[0]
        return {"token":token}


    # 正则表达式的函数封装，获取Handler里面的 “@property” 的值。注意，“@property”的函数名称必须与excel 里要替换的#xxx# 对应,否则取不到值。
    def replace_data(self,data):
        """ 正则封装，通过正则获取并替换 用例里面需要替换的数据。 """
        # 导入
        import re
        # 设置正则表达式匹配规则
        patten = r"#(.+?)#"
        while re.search(patten,data):
            key = re.search(patten,data).group(1)
            value = getattr(self,key,"")
            data = re.sub(patten,str(value),data,1)
        return data

if __name__ == '__main__':
    pass

    # # 打印配置文件数据
    # data_path = HandLer.conf.DATA_PATH
    # print(data_path)
    # # 打印 yaml 数据
    # yaml_data = HandLer.yaml
    # print(yaml_data["excel"]["file"])
    # 打印excel 对象
    # print(HandLer.excel.read_data("Sheet1"))
    # # # 打印logger日志
    # print(HandLer.logger.info("这是 info 级别 日志"))
    # HandLer.logger.error("这是 error 级别 日志")

    # 访问登录接口
    # print(HandLer().login(user=HandLer.yaml["user"]))
    # print(HandLer().token)

    # 使用正则替换数据，
    # 正则表达式的函数封装，获取Handler里面的 “@property” 的值。注意，“@property”的函数名称必须与excel 里要替换的#xxx# 对应。
    # h = HandLer()
    # m_str = '{"id":"#id#","token":"#token#"}'
    # a = h.replace_data(m_str)
    # print(a)

