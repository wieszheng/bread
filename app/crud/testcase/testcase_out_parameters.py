# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/12 12:51
@Author   : wiesZheng
@Software : PyCharm
"""

from typing import List

from app.crud import BaseCRUD
from app.models.out_parameters import TestCaseOutParameters
from app.schemas.testcase.testcase_out_parameters import TestCaseParametersParam


class TestCaseOutParametersCRUD(BaseCRUD):
    __model__ = TestCaseOutParameters

    @classmethod
    async def update_many(cls, case_id: int, user_id: int, data: List[TestCaseParametersParam]):
        pass
