# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 11:50
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import Any

from fastapi import HTTPException

from app.commons.response.response_code import CustomErrorCode


class CustomException(Exception):
    __slots__ = ["err_code", "err_code_des"]

    def __init__(
        self,
        result: CustomErrorCode = None,
        err_code: int = 0000,
        err_code_des: str = "",
    ):
        if result:
            self.err_code = result.code
            self.err_code_des = err_code_des or result.msg
        else:
            self.err_code = err_code
            self.err_code_des = err_code_des
        super().__init__(self)


class DBError(Exception):
    pass


class HTTPError(HTTPException):
    def __init__(
        self, *, code: int, msg: Any = None, headers: dict[str, Any] | None = None
    ):
        super().__init__(status_code=code, detail=msg, headers=headers)


class ForbiddenError(Exception):
    pass


class NotFoundError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class TokenError(Exception):
    pass
    # def __init__(self, *, msg: str = 'Not Authenticated', headers: dict[str, Any] | None = None):
    #     super().__init__(detail=msg, headers=headers or {'WWW-Authenticate': 'Bearer'})
