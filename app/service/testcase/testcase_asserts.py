#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 0:40
@Author   : wiesZheng
@Software : PyCharm
"""

from typing import Annotated

from fastapi import Depends

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseModel, ResponseBase
from app.core.security.Jwt import get_current_user_new
from app.crud.testcase.testcase import TestCaseCRUD
from app.crud.testcase.testcase_asserts import TestCaseAssertsCRUD
from app.exceptions.errors import CustomException
from app.schemas.auth.user import CurrentUserInfo
from app.schemas.testcase.testcase_asserts import (
    TestCaseAssertsParams,
    UpdateTestCaseAssertsParams,
)


class TestCaseAssertsService:
    @staticmethod
    async def create_asserts(
        obj: TestCaseAssertsParams,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_case = await TestCaseCRUD.get(id=obj.case_id)
        if not input_case:
            raise CustomException(CustomErrorCode.CASE_ID_NOT_EXIST)
        input_ = await TestCaseAssertsCRUD.exists(
            case_id=obj.case_id, name=obj.name, is_deleted=False
        )
        if input_:
            raise CustomException(CustomErrorCode.CASE_ASSERTS_EXIST)
        result = await TestCaseAssertsCRUD.create(obj=obj, created_by=user_info.id)
        return await ResponseBase.success(result=result.to_dict())

    @staticmethod
    async def update_asserts(
        obj: UpdateTestCaseAssertsParams,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_ = await TestCaseAssertsCRUD.exists(id=obj.id, is_deleted=False)
        if not input_:
            raise CustomException(CustomErrorCode.CASE_ASSERTS_NOT_EXIST)
        result = await TestCaseAssertsCRUD.update(
            obj={**obj.model_dump(), 'updated_by': user_info.id}, id=obj.id
        )
        return await ResponseBase.success(result=result)

    @staticmethod
    async def delete_asserts(asserts_id: Annotated[int, ...]) -> ResponseModel:
        input_ = await TestCaseAssertsCRUD.exists(id=asserts_id, is_deleted=False)
        if not input_:
            raise CustomException(CustomErrorCode.CASE_ASSERTS_NOT_EXIST)
        await TestCaseAssertsCRUD.delete(id=asserts_id)
        return await ResponseBase.success()
