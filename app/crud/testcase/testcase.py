# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 19:03
@Author   : wiesZheng
@Software : PyCharm
"""
from app.crud import BaseCRUD
from app.models.test_case import TestCase


class TestCaseCRUD(BaseCRUD):
    __model__ = TestCase

    pass
