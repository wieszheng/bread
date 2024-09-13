#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 22:52
@Author   : wiesZheng
@Software : PyCharm
"""

from typing import Optional

from pydantic import BaseModel, Field

from app.commons.response.response_schema import ListPageRequestModel


class EnvironmentSchemaBase(BaseModel):
    name: str = Field(..., description='环境名称')
    remarks: str | None = None


class UpdateEnvironmentParam(EnvironmentSchemaBase):
    id: int


class EnvironmentQuery(BaseModel):
    name: Optional[str] = Field(default=None, description='环境名称')


class EnvironmentListInParam(ListPageRequestModel):
    pass
