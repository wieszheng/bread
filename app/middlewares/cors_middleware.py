# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 11:39
@Author   : wiesZheng
@Software : PyCharm
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(_app: FastAPI):
    # 前端页面url

    # 后台api允许跨域
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],  # 允许的来源，可以是字符串、字符串列表，或通配符 "*"
        allow_credentials=True,  # 是否允许携带凭证（例如，使用 HTTP 认证、Cookie 等）
        allow_methods=['*'],  # 允许的 HTTP 方法，可以是字符串、字符串列表，或通配符 "*"
        allow_headers=[
            '*'
        ],  # 允许的 HTTP 头信息，可以是字符串、字符串列表，或通配符 "*"
        expose_headers=['*'],  # 允许前端访问的额外响应头，可以是字符串、字符串列表
    )
