
# TODO:日志的封装

import logging

# 定义一个 test_cases_logging 函数
def test_cases_logging(
        name = None,
        file = None,
        root_level = "DEBUG",
        starm_level = "INFO",
        file_level = "INFO",
        fmt = '%(asctime)s--%(filename)s--%(lineno)d--%(levelname)s:%(message)s',
):
    # 初始化一个收集器
    root_logging = logging.getLogger(name)
    # 设置收集器的等级
    root_logging.setLevel(root_level)
    # 初始化一个控制台输出器
    starm_handler = logging.StreamHandler()
    # 设置控制台输出器的等级
    starm_handler.setLevel(starm_level)
    # 把输出器添加到收集器上面
    root_logging.addHandler(starm_handler)
    # 设置日志格式
    fmt = logging.Formatter(fmt)
    starm_handler.setFormatter(fmt)
    # 判断file是否传值，
    if file:
        # 初始化一个文本输出器
        file_handler = logging.FileHandler(file,encoding="utf8")
        # 设置文本输出器的等级
        file_handler.setLevel(file_level)
        # 把输出器添加到收集器上面
        root_logging.addHandler(file_handler)
        # 设置日志格式
        file_handler.setFormatter(fmt)
    return root_logging
# root_logging = test_cases_logging(file = "caser.txt")
if __name__ == '__main__':
    pass


