#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/13 23:11
@Author   : wiesZheng
@Software : PyCharm
"""

from pydantic import BaseModel


class TestCaseAssertsParams(BaseModel):
    name: str
    case_id: int = None
    assert_type: str
    expected: str
    actually: str


class UpdateTestCaseAssertsParams(TestCaseAssertsParams):
    id: int
