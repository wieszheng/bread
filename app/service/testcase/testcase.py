#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 0:06
@Author   : wiesZheng
@Software : PyCharm
"""

from typing import Annotated

from fastapi import Depends

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.core.security.Jwt import get_current_user_new
from app.crud.testcase.testcase import TestCaseCRUD
from app.crud.testcase.testcase_asserts import TestCaseAssertsCRUD
from app.crud.testcase.testcase_directory import TestcaseDirectoryCRUD
from app.exceptions.errors import CustomException
from app.models.testcase_asserts import TestCaseAsserts
from app.models.testcase_data import TestCaseData
from app.schemas.auth.user import CurrentUserInfo
from app.schemas.testcase.testcase import (
    TestCaseInfoParam,
    TestCaseParam,
    TestCaseSchemaBase,
)


class TestCaseService:
    @staticmethod
    async def get_testcase_list(
        directory_id: Annotated[int | None, ...] = None,
        name: Annotated[str, ...] = '',
        create_user: Annotated[str | None, ...] = None,
    ) -> ResponseModel:
        parents = []
        if directory_id:
            parents = await TestcaseDirectoryCRUD.get_directory_son(directory_id)
        result = await TestCaseCRUD.get_multi_by_cursor(
            directory_id__in=parents, name__startswith=name, created_by=create_user
        )

        return await ResponseBase.success(result=result)

    @staticmethod
    async def add_testcase(
        obj: TestCaseSchemaBase,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_ = await TestCaseCRUD.exists(name=obj.name, directory_id=obj.directory_id)
        if input_:
            raise CustomException(CustomErrorCode.CASE_NAME_EXIST)
        result = await TestCaseCRUD.create(obj=obj, created_by=user_info.id)
        return await ResponseBase.success(result=result.to_dict())

    @staticmethod
    async def create_testcase(
        obj: TestCaseInfoParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_ = await TestCaseCRUD.exists(directory_id=obj.case.directory_id, name=obj.case.name)
        if input_:
            raise CustomException(CustomErrorCode.CASE_NAME_EXIST)
        result = await TestCaseCRUD.create(obj=obj.case, created_by=user_info.id, commit=False)
        await TestCaseCRUD._insert(
            case_id=result.id,
            user_id=user_info.id,
            obj=obj,
            asserts=(TestCaseAssertsCRUD, TestCaseAsserts),
            data=(TestCaseCRUD, TestCaseData),
        )
        return await ResponseBase.success(result=result.to_dict())

    @staticmethod
    async def update_testcase(
        obj: TestCaseParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_id = await TestCaseCRUD.get(id=obj.id)
        if input_id:
            raise CustomException(CustomErrorCode.CASE_ID_NOT_EXIST)
        await TestCaseCRUD.update(
            obj={**obj.model_dump(), 'updated_by': user_info.id},
            id=obj.id,
        )

        return await ResponseBase.success()

    @staticmethod
    async def delete_testcase(id: int):
        pass

    @staticmethod
    async def get_testcase(id: int):
        pass

    @staticmethod
    async def get_xmind(id: int):
        pass

    @staticmethod
    async def move_testcase(id: int):
        pass

    @staticmethod
    async def get_record_start(id: int):
        pass

    @staticmethod
    async def get_record_stop(id: int):
        pass

    @staticmethod
    async def get_record_status(id: int):
        pass

    @staticmethod
    async def get_record_remove(id: int):
        pass

    @staticmethod
    async def create_generate(id: int):
        pass

    @staticmethod
    async def testcase_import(id: int):
        pass

    @staticmethod
    async def get_variables(id: int):
        pass
