# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/12 12:40
@Author   : wiesZheng
@Software : PyCharm
"""
from pydantic import BaseModel, Field


class ResponseBaseModel(BaseModel):
    """ 统一响应模型 """
    code: int
    success: bool
    message: str
    result: dict


class ListResponseDataModel(BaseModel):
    """ 分页列表响应data模型 """
    total: int = Field(default=0, description="数据总数量")
    data_list: list = Field(default=[], description='数据列表')
    has_more: bool = Field(default=False, description="是否有下一页")
    next_offset: int = Field(default=0, description="offset下次起步")


class ListResponseModel(ResponseBaseModel):
    """ 分页列表响应统一返回 """
    data: ListResponseDataModel


class SuccessModel(ResponseBaseModel):
    """ 请求成功响应模型 """
