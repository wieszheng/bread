#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/12 0:12
@Author   : wiesZheng
@Software : PyCharm
"""

from typing import List

from app.crud import BaseCRUD
from app.models.testcase_asserts import TestCaseAsserts


class TestCaseAssertsCRUD(BaseCRUD):
    __model__ = TestCaseAsserts

    @classmethod
    async def delete_records(cls, id_list: List[int], column='id'):
        for id_ in id_list:
            input_ = await cls.exists(**{column: id_})
            if not input_:
                continue
            await cls.delete(**{column: id_})
