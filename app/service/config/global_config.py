# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 15:04
@Author   : wiesZheng
@Software : PyCharm
"""
from app.commons.response.response_schema import ResponseBase, ResponseModel


class GlobalConfigService:
    @staticmethod
    async def create_global_config(obj) -> ResponseModel:
        return await ResponseBase.success()
