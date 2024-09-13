# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 16:05
@Author   : wiesZheng
@Software : PyCharm
"""

from typing import Optional

from pydantic import BaseModel, Field

from app.commons.response.response_schema import ListPageRequestModel


class AddressSchemaBase(BaseModel):
    env: int
    name: str
    gateway: str


class UpdateAddressParam(AddressSchemaBase):
    id: int


class AddressQuery(BaseModel):
    env: Optional[int] = Field(default=None, description='环境')
    name: Optional[str] = Field(default=None, description='环境名称')


class AddressListInParam(ListPageRequestModel):
    query_params: Optional[AddressQuery] = Field(default={}, description='查询参数')
