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
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.core.security.Jwt import get_current_user_new
from app.crud.testcase.constructor import ConstructorCRUD
from app.crud.testcase.testcase import TestCaseCRUD
from app.exceptions.errors import CustomException
from app.schemas.auth.user import CurrentUserInfo
from app.schemas.testcase.constructor import ConstructorParams, UpdateConstructorParams


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
    async def get_constructor(id: int):
        pass

    @staticmethod
    async def get_constructor_list(id: int):
        pass

    @staticmethod
    async def update_constructor_order(id: int):
        pass

    @staticmethod
    async def get_constructor_tree(id: int):
        pass
