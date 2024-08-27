# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 15:02
@Author   : wiesZheng
@Software : PyCharm
"""
from app.commons.response.response_schema import ResponseBase, ResponseModel


class EnvironmentService:

    @staticmethod
    async def create_environment(obj) -> ResponseModel:
        return await ResponseBase.success()

    @staticmethod
    async def get_environment(obj) -> ResponseModel:
        return await ResponseBase.success()

    @staticmethod
    async def delete_environment(obj) -> ResponseModel:
        return await ResponseBase.success()

    @staticmethod
    async def update_environment(obj) -> ResponseModel:
        return await ResponseBase.success()

    @staticmethod
    async def get_environments(obj) -> ResponseModel:
        return await ResponseBase.success()
