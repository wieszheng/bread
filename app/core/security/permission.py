# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/16 10:48
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import Request

from config import AppConfig


class RequestPermission:
    """
    请求权限

    Tip:
        使用此请求权限时，需要将 `Depends(RequestPermission('xxx'))` 在 `DependsRBAC` 之前设置，
        因为 fastapi 当前版本的接口依赖注入按正序执行，意味着 RBAC 标识会在验证前被设置
    """

    def __init__(self, role: int):
        self.role = role

    async def __call__(self, request: Request):
        if AppConfig.ADMIN == 2:
            if not isinstance(self.role, str):
                raise Exception
            # 附加权限标识
            request.state.permission = self.role
