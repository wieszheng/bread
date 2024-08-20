# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/16 10:48
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import Request

from app.exceptions.errors import AuthorizationError
from config import settings


class RequestPermission:
    """
    请求权限

    """

    def __init__(self, role: int):
        self.role = role

    async def __call__(self, request: Request):
        user_role = request.user.role
        if user_role < self.role:
            raise AuthorizationError('对不起, 你没有足够的权限')
