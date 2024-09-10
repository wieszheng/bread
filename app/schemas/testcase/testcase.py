# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 19:07
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import List, Annotated

from pydantic import BaseModel, Field

from app.schemas.testcase.testcase_out_parameters import TestCaseOutParametersForm


class TestCaseSchemaBase(BaseModel):
    priority: Annotated[str, Field(min_length=2, max_length=30)]
    url: str = ""
    name: str = ""
    case_type: int = 0
    base_path: str = None
    tag: str = None
    body: str = None
    body_type: int = 0
    request_headers: str = None
    request_method: str = None
    status: int
    out_parameters: List[TestCaseOutParametersForm] = []
    directory_id: int
    request_type: int


class TestCaseParam(TestCaseSchemaBase):
    id: int = None
