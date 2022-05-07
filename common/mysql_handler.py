
# TODO:Mysql的封装，查询数据库的封装


import pymysql
from pymysql.cursors import DictCursor
# 游标类，默认查询出的数据是元组格式，通过 DictCursor 把数据转换成 字典格式

# 定义一个 MysqlHandler 类
class MysqlHandler():
    """ 初始化连接数据库的配置参数 """
    def __init__(
            self,
            host=None,
            port=3306,
            user=None,
            passwd=None,
            charset='utf8',
            cursorclass=DictCursor
    ):
        self.conne = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            charset=charset,
            cursorclass=cursorclass
        )
        # 初始化游标,写测试方法时，用来查询数据库 数据插入前的数据
        self.cursor = self.conne.cursor()

    def query(self,sql,one = True):
        self.conne.commit()  # 把最新的数据进行更新（提交事务），每次查询前，把查询前的事务提交
        self.cursor.execute(sql)
        # 条件判断，默认变量“one” = True，如果one=True，则返回一行数据，否则返回多行数据。
        if one:
            return self.cursor.fetchone()
        return self.cursor.fetchall()

    # 每次查询完后关闭数据库
    def close(self):
        # 游标对象关闭
        self.cursor.close()
        # 连接对象关闭
        self.conne.cursor()
if __name__ == '__main__':
        pass

