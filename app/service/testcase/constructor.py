#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 0:40
@Author   : wiesZheng
@Software : PyCharm
"""

from collections import defaultdict
from typing import Annotated, List

from fastapi import Depends

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.core.security.Jwt import get_current_user_new
from app.crud.testcase.constructor import ConstructorCRUD
from app.crud.testcase.testcase import TestCaseCRUD
from app.exceptions.errors import CustomException
from app.schemas.auth.user import CurrentUserInfo
from app.schemas.testcase.constructor import (
    ConstructorParams,
    UpdateConstructorParams,
    ConstructorIndexParams,
)


class ConstructorService:
    @staticmethod
    async def create_constructor(
        obj: ConstructorParams,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_case = await TestCaseCRUD.get(id=obj.case_id)
        if not input_case:
            raise CustomException(CustomErrorCode.CASE_ID_NOT_EXIST)
        input_ = await ConstructorCRUD.exists(
            case_id=obj.case_id, name=obj.name, is_deleted=False
        )
        if input_:
            raise CustomException(CustomErrorCode.CASE_CONSTRUCTOR_EXIST)
        result = await ConstructorCRUD.create(obj=obj, created_by=user_info.id)
        return await ResponseBase.success(result=result.to_dict())

    @staticmethod
    async def update_constructor(
        obj: UpdateConstructorParams,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_ = await ConstructorCRUD.exists(id=obj.id, is_deleted=False)
        if not input_:
            raise CustomException(CustomErrorCode.CASE_CONSTRUCTOR_NOT_EXIST)
        await ConstructorCRUD.update(
            obj={**obj.model_dump(), 'updated_by': user_info.id}, id=obj.id
        )
        return await ResponseBase.success()

    @staticmethod
    async def delete_constructor(id: Annotated[int, ...]) -> ResponseModel:
        input_ = await ConstructorCRUD.exists(id=id, is_deleted=False)
        if not input_:
            raise CustomException(CustomErrorCode.CASE_CONSTRUCTOR_NOT_EXIST)
        await ConstructorCRUD.delete(id=id)
        return await ResponseBase.success()

    @staticmethod
    async def get_constructor(id: Annotated[int, ...]) -> ResponseModel:
        input_ = await ConstructorCRUD.exists(id=id, is_deleted=False)
        if not input_:
            raise CustomException(CustomErrorCode.CASE_CONSTRUCTOR_NOT_EXIST)
        result = await ConstructorCRUD.get(id=id)
        return await ResponseBase.success(result=result)

    @staticmethod
    async def get_constructor_list(
        constructor_type: Annotated[int, ...], suffix: Annotated[bool, ...]
    ) -> ResponseModel:
        ans = list()
        constructors = defaultdict(list)
        result_all = await ConstructorCRUD.get_all(
            suffix=suffix, type=constructor_type, public=True, is_deleted=False
        )
        for item in result_all['data']:
            constructors[item['case_id']].append({
                'title': item['name'],
                'key': f"constructor_{item['id']}",
                'value': f"constructor_{item['id']}",
                'isLeaf': True,
                'constructor_json': item['constructor_json'],
            })
        if len(constructors.keys()) == 0:
            return await ResponseBase.success(result={'data': []})
        result_all = await TestCaseCRUD.get_all(
            id__in=list(constructors.keys()), is_deleted=False
        )
        for item in result_all['data']:
            ans.append({
                'title': item['name'],
                'key': f"caseId_{item['id']}",
                'disabled': True,
                'children': constructors[item['id']],
            })
        return await ResponseBase.success(result={'data': ans})

    @staticmethod
    async def update_constructor_order(
        data: Annotated[List[ConstructorIndexParams], ...],
    ) -> ResponseModel:
        for item in data:
            await ConstructorCRUD.update(obj={'index': item.index}, id=item.id)
        return await ResponseBase.success()

    @staticmethod
    async def get_constructor_tree(
        suffix: Annotated[bool, ...],
        name: Annotated[str, ...] = '',
    ) -> ResponseModel:
        result = await ConstructorCRUD.get_all(
            suffix=suffix, public=True, is_deleted=False, name__startswith=name
        )
        if not result['data']:
            return await ResponseBase.success(result={'data': []})
        temp = defaultdict(list)
        # 建立caseID -> constructor的map
        for c in result['data']:
            temp[c['case_id']].append(c)
        result_all = await TestCaseCRUD.get_all(
            id__in=list(temp.keys()), is_deleted=False
        )
        testcase_info = {t['id']: t for t in result_all['data']}
        result = []
        for k, v in temp.items():
            result.append({
                'title': testcase_info[k]['name'],
                'key': f'caseId_{k}',
                'disabled': True,
                'children': [
                    {
                        'key': f"constructor_{item['id']}",
                        'title': item['name'],
                        'value': f"constructor_{item['id']}",
                    }
                    for item in v
                ],
            })
        return await ResponseBase.success(result={'data': result})
