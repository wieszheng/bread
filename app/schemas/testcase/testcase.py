# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 19:07
@Author   : wiesZheng
@Software : PyCharm
"""

from typing import Annotated

from pydantic import BaseModel, Field


class TestCaseSchemaBase(BaseModel):
    name: str = ""
    priority: Annotated[str, Field(min_length=1, max_length=3)]
    url: str = ""
    case_type: int = 0
    base_path: str = None
    tag: str = None
    body: str = None
    body_type: int = 0
    request_headers: str = None
    request_method: str = None
    status: int
    directory_id: int
    request_type: int


class TestCaseParam(TestCaseSchemaBase):
    id: int = None
