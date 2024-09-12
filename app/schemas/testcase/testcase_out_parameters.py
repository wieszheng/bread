# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 19:36
@Author   : wiesZheng
@Software : PyCharm
"""

from pydantic import BaseModel


class TestCaseOutSchemaBase(BaseModel):
    name: str
    expression: str = None
    match_index: str = None
    source: int


class TestCaseParametersParam(TestCaseOutSchemaBase):
    id: int = None
    case_id: int = None


class TestCaseVariablesParam(BaseModel):
    case_id: int
    step_name: str
