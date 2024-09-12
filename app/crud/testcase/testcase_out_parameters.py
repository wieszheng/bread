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
from app.schemas.testcase.testcase_out_parameters import UpdateTestCaseParametersParam


class TestCaseOutParametersCRUD(BaseCRUD):
    __model__ = TestCaseOutParameters

    @classmethod
    async def should_remove(cls, before, after):
        """
        删除的数据
        """
        data = []
        for b in before:
            if b["id"] not in after:
                data.append(b["id"])
        return data

    @classmethod
    async def update_many(cls, case_id: int, user_id: int, data: List[UpdateTestCaseParametersParam]):
        result = []
        source = await cls.get_multi_by_cursor(case_id=case_id)
        before = source["data"]
        if data:
            for item in data:
                temp = await cls.get(name=item.name, case_id=case_id)
                if temp is None:
                    temp = await cls.create(obj=item, case_id=case_id, created_by=user_id)
                    result.append({**item.model_dump(), **temp.to_dict()})
                else:
                    temp["name"] = item.name
                    temp["expression"] = item.expression
                    temp["source"] = item.source
                    temp["match_index"] = item.match_index
                    await cls.update(obj={**temp, "updated_by": user_id}, id=temp["id"])
                    result.append({**item.model_dump(), **temp})

            should_remove = await cls.should_remove(before, [x["id"] for x in result])
            print(should_remove)
            if should_remove:
                await cls.delete(allow_multiple=True, id__in=should_remove)

            return result
