
import unittest
import os
from datetime import datetime
from setting import config
from libs.HTMLTestRunnerNew import HTMLTestRunner

# 初始化一个用例加载器
loader = unittest.TestLoader()
# 收集用例
suite = loader.discover(config.CASE_PATH)
# 测试报告路径
ts = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
new_file_path = 'test{}.html'.format(ts)
file_path = os.path.join(config.RESPONSE_PATH, new_file_path)

# 执行用例
with open(file_path,mode='wb') as f:
    new_run = HTMLTestRunner(
        f,
        title='测试报告标题',
        description = '干脆面的测试报告'
    )
    new_run.run(suite)


