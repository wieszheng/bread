# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/11 12:15
@Author   : wiesZheng
@Software : PyCharm
"""
from collections import defaultdict
from typing import Annotated

from app.crud import BaseCRUD
from app.models.testcase_directory import TestcaseDirectory


class TestcaseDirectoryCRUD(BaseCRUD):
    __model__ = TestcaseDirectory

    @classmethod
    def get_sub_son(cls, parent_map: dict, son: list, result: list):
        if not son:
            return
        for s in son:
            result.append(s)
            sons = parent_map.get(s)
            if not sons:
                continue
            result.extend(sons)
            cls.get_sub_son(parent_map, sons, result)

    @classmethod
    async def get_directory_son(cls, directory_id: Annotated[int | None, ...]):
        parent_map = defaultdict(list)
        ans = [directory_id]
        result = await cls.get_multi_by_cursor(parent__or={"eq": directory_id, "ne": None})
        for d in result["data"]:
            parent_map[d["parent"]].append(d["id"])
        son = parent_map.get(directory_id)
        cls.get_sub_son(parent_map, son, ans)
        return ans
