# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/11 12:15
@Author   : wiesZheng
@Software : PyCharm
"""

from collections import defaultdict

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
    async def get_directory_son(cls, directory_id: int):
        parent_map = defaultdict(list)
        ans = [directory_id]
        result = await cls.get_multi_by_cursor(
            parent__or={'eq': directory_id, 'ne': None}
        )
        for d in result['data']:
            parent_map[d['parent']].append(d['id'])
        son = parent_map.get(directory_id)
        cls.get_sub_son(parent_map, son, ans)
        return ans

    @classmethod
    async def get_directory_list(cls, project_id: int):
        return await cls.get_multi_by_cursor(project_id=project_id, is_deleted=False)

    @classmethod
    async def get_directory(
        cls,
        ans_map: dict,
        parent_map,
        parent,
        children,
        case_map,
        case_node=None,
        move=False,
    ):
        current = parent_map.get(parent)
        if case_node is not None:
            nodes, cs = await case_node(parent)
            children.extend(nodes)
            case_map.update(cs)
        if current is None:
            return
        for c in current:
            temp = ans_map.get(c)
            if case_node is None:
                child = list()
            else:
                child, cs = await case_node(temp.id)
                case_map.update(cs)
            children.append(
                dict(
                    title=temp['name'],
                    key=temp['id'],
                    children=child,
                    label=temp['name'],
                    value=temp['id'],
                    disabled=len(child) == 0 and not move,
                )
            )
            await cls.get_directory(
                ans_map, parent_map, temp['id'], child, case_node, move=move
            )
