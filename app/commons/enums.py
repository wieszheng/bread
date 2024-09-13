#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/17 11:24
@Author   : wiesZheng
@Software : PyCharm
"""

from enum import Enum, IntEnum


class RoleType(IntEnum):
    """权限"""

    MEMBER = 0
    MANAGER = 1
    ADMIN = 2


class HttpMethod(Enum):
    """
    请求方式
    """

    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'


class RespFmt(Enum):
    """http响应格式"""

    JSON = 'json'
    BYTES = 'bytes'
    TEXT = 'text'


class KeyType(Enum):
    """变量属性"""

    STRING = 0
    JSON = 1
    YAML = 2
