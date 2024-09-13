# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 10:44
@Author   : wiesZheng
@Software : PyCharm
"""

import uvicorn

from config import settings

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_RELOAD,
        forwarded_allow_ips='*',
        access_log=False,
    )
