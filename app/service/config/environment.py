# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 15:02
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import Annotated

from fastapi import Request

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.crud.config.environment import EnvironmentCRUD
from app.exceptions.errors import CustomException
from app.schemas.config.environment import (
    EnvironmentListInParam,
    EnvironmentSchemaBase,
    UpdateEnvironmentParam,
)


class EnvironmentService:

    @staticmethod
    async def create_environment(
        request: Request, obj: EnvironmentSchemaBase
    ) -> ResponseModel:
        input_name = await EnvironmentCRUD.exists(name=obj.name, is_deleted=False)
        if input_name:
            raise CustomException(CustomErrorCode.ENVIRONMENT_NAME_EXIST)
        result = await EnvironmentCRUD.create(obj=obj, created_by=request.user.id)
        return await ResponseBase.success(result=result.to_dict())

    @staticmethod
    async def get_environment(env_id: Annotated[int, ...]) -> ResponseModel:
        input_id = await EnvironmentCRUD.exists(id=env_id, is_deleted=False)
        if not input_id:
            raise CustomException(CustomErrorCode.ENVIRONMENT_ID_NOT_EXIST)
        result = await EnvironmentCRUD.get(id=env_id)
        return await ResponseBase.success(result=result)

    @staticmethod
    async def delete_environment(env_id: Annotated[int, ...]) -> ResponseModel:
        input_id = await EnvironmentCRUD.exists(id=env_id, is_deleted=False)
        if not input_id:
            raise CustomException(CustomErrorCode.ENVIRONMENT_ID_NOT_EXIST)
        await EnvironmentCRUD.delete(id=env_id)
        return await ResponseBase.success()

    @staticmethod
    async def update_environment(
        request: Request, obj: UpdateEnvironmentParam
    ) -> ResponseModel:
        input_id = await EnvironmentCRUD.exists(id=obj.id, is_deleted=False)
        if not input_id:
            raise CustomException(CustomErrorCode.ENVIRONMENT_ID_NOT_EXIST)
        input_name = await EnvironmentCRUD.get(name=obj.name, is_deleted=False)
        if input_name and input_name["id"] != obj.id:
            raise CustomException(CustomErrorCode.ENVIRONMENT_NAME_EXIST)
        await EnvironmentCRUD.update(
            obj={**obj.model_dump(), "updated_by": request.user.id}, id=obj.id
        )
        return await ResponseBase.success()

    @staticmethod
    async def get_environments(obj: EnvironmentListInParam) -> ResponseModel:

        result = await EnvironmentCRUD.get_list(
            filter_params=obj.query_params,
            orderings=obj.orderings,
            limit=obj.page_size,
            offset=obj.page,
        )

        return await ResponseBase.success(
            result={**result, "page": obj.page, "page_size": obj.page_size}
        )
