# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 12:40
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import FastAPI

from app.middlewares.cors_middleware import add_cors_middleware
from app.middlewares.custom_middleware import add_custom_middleware


def register_middlewares(app: FastAPI):
    """
    全局中间件处理
    """
    # 加载跨域中间件
    add_cors_middleware(app)
    # 自定义
    add_custom_middleware(app)
