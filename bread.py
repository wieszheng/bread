# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 10:44
@Author   : wiesZheng
@Software : PyCharm
"""
import uvicorn

from config import AppConfig

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=AppConfig.APP_HOST,
        port=AppConfig.APP_PORT,
        reload=AppConfig.APP_RELOAD,
        forwarded_allow_ips="*",
        access_log=False,
    )
