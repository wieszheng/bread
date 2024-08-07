# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 11:39
@Author   : wiesZheng
@Software : PyCharm
"""
from starlette.middleware.cors import CORSMiddleware

from .middlewares import LoggingMiddleware
from fastapi import FastAPI


def register_middlewares(_app: FastAPI):
    """注册中间件"""
    middleware_list = [
        LoggingMiddleware
    ]
    for middleware in middleware_list:
        _app.add_middleware(middleware)

    # 前端页面url
    origins = [
        "http://localhost:8088",
        "http://127.0.0.1:8088",
    ]

    # 后台api允许跨域
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # 允许的来源，可以是字符串、字符串列表，或通配符 "*"
        allow_credentials=True,  # 是否允许携带凭证（例如，使用 HTTP 认证、Cookie 等）
        allow_methods=["*"],  # 允许的 HTTP 方法，可以是字符串、字符串列表，或通配符 "*"
        allow_headers=["*"],  # 允许的 HTTP 头信息，可以是字符串、字符串列表，或通配符 "*"
        expose_headers=["*"],  # 允许前端访问的额外响应头，可以是字符串、字符串列表
    )
