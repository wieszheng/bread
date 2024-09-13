# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 19:07
@Author   : wiesZheng
@Software : PyCharm
"""

from typing import Annotated, List

from pydantic import BaseModel, Field

from app.schemas.testcase.testcase_data import TestcaseDataParam
from app.schemas.testcase.testcase_out_parameters import (
    TestCaseParametersParam,
    UpdateTestCaseParametersParam,
)


class TestCaseSchemaBase(BaseModel):
    name: str = ''
    priority: Annotated[str, Field(min_length=1, max_length=3)]
    url: str = ''
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


class UpdateTestCaseParam(TestCaseSchemaBase):
    out_parameters: List[UpdateTestCaseParametersParam] = []
    id: int = None


class TestCaseAssertsParam(BaseModel):
    id: int = None
    name: str
    case_id: int = None
    assert_type: str
    expected: str
    actually: str


class TestCaseInfoParam(BaseModel):
    case: TestCaseSchemaBase = None
    asserts: List[TestCaseAssertsParam] = []
    data: List[TestcaseDataParam] = []
    # constructor: List[ConstructorForm] = []
    out_parameters: List[TestCaseParametersParam] = []
