#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 0:38
@Author   : wiesZheng
@Software : PyCharm
"""

from collections import defaultdict
from typing import Annotated

from fastapi import Depends

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseModel, ResponseBase
from app.core.security.Jwt import get_current_user_new
from app.crud.testcase.testcase_directory import TestcaseDirectoryCRUD
from app.exceptions.errors import CustomException
from app.schemas.auth.user import CurrentUserInfo
from app.schemas.testcase.testcase_directory import (
    TestcaseDirectoryParams,
    UpdateTestcaseDirectoryParams,
)


class TestcaseDirectoryService:
    @staticmethod
    async def create_directory(
        obj: TestcaseDirectoryParams,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_ = await TestcaseDirectoryCRUD.exists(
            name=obj.name,
            parent=obj.parent,
            project_id=obj.project_id,
            is_deleted=False,
        )
        if input_:
            raise CustomException(CustomErrorCode.CASE_DIRECTORY_EXIST)
        result = await TestcaseDirectoryCRUD.create(obj=obj, created_by=user_info.id)
        return await ResponseBase.success(result=result.to_dict())

    @staticmethod
    async def update_directory(
        obj: UpdateTestcaseDirectoryParams,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_ = await TestcaseDirectoryCRUD.exists(id=obj.id, is_deleted=False)
        if not input_:
            raise CustomException(CustomErrorCode.CASE_DIRECTORY_NOT_EXIST)
        await TestcaseDirectoryCRUD.update(
            obj={**obj.model_dump(), 'updated_by': user_info.id}, id=obj.id
        )
        return await ResponseBase.success()

    @staticmethod
    async def delete_directory(id: Annotated[int, ...]) -> ResponseModel:
        input_ = await TestcaseDirectoryCRUD.exists(id=id, is_deleted=False)
        if not input_:
            raise CustomException(CustomErrorCode.CASE_DIRECTORY_NOT_EXIST)
        await TestcaseDirectoryCRUD.delete(id=id)
        return await ResponseBase.success()

    @staticmethod
    async def get_directory(
        project_id: Annotated[int, ...],
        case_node=None,
        move: Annotated[bool, ...] = False,
    ) -> ResponseModel:
        result = await TestcaseDirectoryCRUD.get_directory_list(project_id=project_id)
        ans = list()
        ans_map = dict()
        case_map = dict()
        parent_map = defaultdict(list)
        for directory in result['data']:
            if directory['parent'] is None:
                ans.append(
                    dict(
                        title=directory['name'],
                        key=directory['id'],
                        value=directory['id'],
                        label=directory['name'],
                        children=list(),
                    )
                )
            else:
                parent_map[directory['parent']].append(directory['id'])
            ans_map[directory['id']] = directory
        for r in ans:
            await TestcaseDirectoryCRUD.get_directory(
                ans_map,
                parent_map,
                r.get('key'),
                r.get('children'),
                case_map,
                case_node,
                move,
            )
            if not move and not r.get('children'):
                r['disabled'] = True
        return await ResponseBase.success(result={'data': ans})

    @staticmethod
    async def get_tree(id: int):
        pass
