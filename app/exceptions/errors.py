# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 11:50
@Author   : wiesZheng
@Software : PyCharm
"""

from fastapi import HTTPException

from app.commons.response.response_code import CustomErrorCode, StandardResponseCode


class CustomException(Exception):
    __slots__ = ['err_code', 'err_code_des']

    def __init__(
        self,
        result: CustomErrorCode = None,
        err_code: int = 0000,
        err_code_des: str = '',
    ):
        if result:
            self.err_code = result.code
            self.err_code_des = err_code_des or result.msg
        else:
            self.err_code = err_code
            self.err_code_des = err_code_des
        super().__init__(self)


class AuthorizationException(HTTPException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(status_code=StandardResponseCode.HTTP_200, detail=self.message)


class PermissionException(HTTPException):
    def __init__(self, message: str = '请求权限不足'):
        self.message = message
        super().__init__(status_code=StandardResponseCode.HTTP_200, detail=self.message)


class DBError(Exception):
    def __init__(self, message: str = ''):
        self.message = message
        super().__init__(self.message)


class TokenError(Exception):
    def __init__(self, message: str = ''):
        self.message = message
        super().__init__(self.message)
