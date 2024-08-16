# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 11:50
@Author   : wiesZheng
@Software : PyCharm
"""
from app.commons.response.response_code import CustomErrorCode


class BusinessException(Exception):
    """ 业务异常类 """

    __slots__ = ['err_code', 'err_code_des']

    def __init__(self, result: CustomErrorCode = None, err_code: str = "0000", err_code_des: str = ""):
        if result:
            self.err_code = result.code
            self.err_code_des = err_code_des or result.msg
        else:
            self.err_code = err_code
            self.err_code_des = err_code_des
        super().__init__(self)


class AuthException(Exception):
    """
    自定义令牌异常AuthException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class PermissionException(Exception):
    """
    自定义权限异常PermissionException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class DBException(Exception):
    """
    自定义令数据库DBException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message
