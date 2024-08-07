# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:54
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import FastAPI
from loguru import logger

from app.apis.v1 import v1


async def register_routers(_app: FastAPI):
    logger.info("注册路由")
    _app.include_router(v1, prefix="/api")
