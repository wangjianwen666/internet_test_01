
# TODO:接口请求方法的封装

import requests

# 定义一个 new_requests 函数，请求接口的函数
def new_requests(
        url,
        method,
        data=None,
        json=None,
        headers=None,
        **kwargs
):
    res = requests.request(
        method,
        url,
        data=data,
        json=json,
        headers=headers,
        **kwargs
    )
    # 条件判断，默认返回的是json格式数据，如果不是，则抛出异常
    try:
        return res.json()
    except Exception as f:
        return '返回的不是json格式：{}'.format(f)


if __name__ == '__main__':
    pass


