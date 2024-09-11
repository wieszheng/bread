# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/11 12:15
@Author   : wiesZheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.models.testcase_directory import TestcaseDirectory


class TestcaseDirectoryCRUD(BaseCRUD):
    __model__ = TestcaseDirectory

    pass
