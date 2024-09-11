#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/12 0:12
@Author   : wiesZheng
@Software : PyCharm
"""
from app.crud import BaseCRUD
from app.models.testcase_asserts import TestCaseAsserts


class TestCaseAssertsCRUD(BaseCRUD):
    __model__ = TestCaseAsserts

    pass
