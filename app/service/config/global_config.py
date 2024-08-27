# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 15:04
@Author   : wiesZheng
@Software : PyCharm
"""
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.schemas.config.global_config import GlobalConfigSchemaBase


class GlobalConfigService:
    @staticmethod
    async def create_global_config(obj: GlobalConfigSchemaBase) -> ResponseModel:
        return await ResponseBase.success()

    @staticmethod
    async def get_global_config(obj) -> ResponseModel:
        return await ResponseBase.success()

    @staticmethod
    async def delete_global_config(obj) -> ResponseModel:
        return await ResponseBase.success()

    @staticmethod
    async def update_global_config(obj) -> ResponseModel:
        return await ResponseBase.success()

    @staticmethod
    async def get_global_configs(obj) -> ResponseModel:
        return await ResponseBase.success()
