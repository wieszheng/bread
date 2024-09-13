#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/13 23:47
@Author   : wiesZheng
@Software : PyCharm
"""

from pydantic import BaseModel


class ConstructorParams(BaseModel):
    value: str = ''
    type: int
    name: str
    constructor_json: str
    enable: bool
    case_id: int = None
    public: bool
    suffix: bool


class UpdateConstructorParams(ConstructorParams):
    id: int


class IndexConstructorParams(ConstructorParams):
    index: int = 0


class ConstructorIndexParams(BaseModel):
    id: int
    index: int
