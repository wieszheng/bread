# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 16:05
@Author   : wiesZheng
@Software : PyCharm
"""

from pydantic import BaseModel


class AddressSchemaBase(BaseModel):
    env: int
    name: str
    gateway: str


class UpdateAddressParam(AddressSchemaBase):
    id: int
