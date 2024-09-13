# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 15:02
@Author   : wiesZheng
@Software : PyCharm
"""

from typing import Annotated

from fastapi import Depends, Query

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.core.security.Jwt import get_current_user_new
from app.crud.config.environment import EnvironmentCRUD
from app.exceptions.errors import CustomException
from app.schemas.auth.user import CurrentUserInfo
from app.schemas.config.environment import EnvironmentSchemaBase, UpdateEnvironmentParam


class EnvironmentService:
    @staticmethod
    async def create_environment(
        obj: EnvironmentSchemaBase,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_name = await EnvironmentCRUD.exists(name=obj.name, is_deleted=False)
        if input_name:
            raise CustomException(CustomErrorCode.ENVIRONMENT_NAME_EXIST)
        result = await EnvironmentCRUD.create(obj=obj, created_by=user_info.id)
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
        obj: UpdateEnvironmentParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_id = await EnvironmentCRUD.exists(id=obj.id, is_deleted=False)
        if not input_id:
            raise CustomException(CustomErrorCode.ENVIRONMENT_ID_NOT_EXIST)
        input_name = await EnvironmentCRUD.get(name=obj.name, is_deleted=False)
        if input_name and input_name['id'] != obj.id:
            raise CustomException(CustomErrorCode.ENVIRONMENT_NAME_EXIST)
        await EnvironmentCRUD.update(
            obj={**obj.model_dump(), 'updated_by': user_info.id}, id=obj.id
        )
        return await ResponseBase.success()

    @staticmethod
    async def get_environments(
        current: Annotated[int, Query(..., ge=1, description='Page number')] = 1,
        pageSize: Annotated[
            int, Query(..., gt=0, le=100, description='Page size')
        ] = 10,
        name: Annotated[str | None, Query(description='环境名称')] = None,
    ) -> ResponseModel:
        result = await EnvironmentCRUD.get_list(
            limit=pageSize, offset=current, name=name
        )

        return await ResponseBase.success(
            result={**result, 'current': current, 'pageSize': pageSize}
        )
