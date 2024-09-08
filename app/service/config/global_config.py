# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 15:04
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import Annotated

from fastapi import Query, Request

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.crud.config.global_config import GlobalConfigCRUD
from app.crud.helper import compute_offset, JoinConfig
from app.exceptions.errors import CustomException
from app.models.environment import Environment
from app.models.user import User
from app.schemas.auth.user import UserInfoSchemaBase
from app.schemas.config.global_config import GlobalConfigSchemaBase, UpdateGlobalConfigParam


class GlobalConfigService:
    @staticmethod
    async def create_global_config(request: Request, obj: GlobalConfigSchemaBase) -> ResponseModel:
        input_data = await GlobalConfigCRUD.exists(
            key=obj.key,
            env=obj.env,
            is_deleted=False
        )
        if input_data:
            raise CustomException(CustomErrorCode.GLOBAL_CONFIG_NAME_EXIST)

        result = await GlobalConfigCRUD.create(obj=obj, created_by=request.user.id)
        return await ResponseBase.success(result=result.to_dict())

    @staticmethod
    async def get_global_config(global_id: Annotated[int, ...]) -> ResponseModel:
        input_id = await GlobalConfigCRUD.get(id=global_id, is_deleted=False)
        if not input_id:
            raise CustomException(CustomErrorCode.GLOBAL_CONFIG_ID_NOT_EXIST)

        return await ResponseBase.success(result=input_id)

    @staticmethod
    async def delete_global_config(global_id: Annotated[int, ...]) -> ResponseModel:
        input_id = await GlobalConfigCRUD.exists(id=global_id, is_deleted=False)
        if not input_id:
            raise CustomException(CustomErrorCode.GLOBAL_CONFIG_ID_NOT_EXIST)
        await GlobalConfigCRUD.delete(id=global_id)
        return await ResponseBase.success()

    @staticmethod
    async def update_global_config(
            request: Request, obj: UpdateGlobalConfigParam
    ) -> ResponseModel:
        input_id = await GlobalConfigCRUD.exists(id=obj.id, is_deleted=False)
        if not input_id:
            raise CustomException(CustomErrorCode.GLOBAL_CONFIG_ID_NOT_EXIST)
        input_data = await GlobalConfigCRUD.exists(
            key=obj.key,
            env=obj.env,
            is_deleted=False
        )
        if input_data:
            raise CustomException(CustomErrorCode.GLOBAL_CONFIG_NAME_EXIST)
        await GlobalConfigCRUD.update(obj={**obj.model_dump(), "updated_by": request.user.id}, id=obj.id)
        return await ResponseBase.success()

    @staticmethod
    async def get_global_configs(
            current: Annotated[int, Query(...)] = 1,
            pageSize: Annotated[int, Query(...)] = 10,
            env_name: Annotated[int | None, Query(description="环境")] = None,
            key: Annotated[str | None, Query(description="key")] = None,
    ) -> ResponseModel:
        filter_params = {}
        if key or env_name:
            filter_params = {"key": key, "env_name": env_name}
        result = await GlobalConfigCRUD.get_multi_joined(
            limit=pageSize,
            offset=compute_offset(current, pageSize),
            sort_columns="id",
            sort_orders="desc",
            joins_config=[
                JoinConfig(
                    model=User,
                    join_on=GlobalConfigCRUD.__model__.created_by == User.id,
                    join_prefix="user_",
                    schema_to_select=UserInfoSchemaBase,
                    join_type="left",
                ),
                JoinConfig(
                    model=Environment,
                    join_on=GlobalConfigCRUD.__model__.env == Environment.id,
                    join_prefix="env_",
                    join_type="left",
                ),
            ],
            is_deleted=False,
            **filter_params
        )
        return await ResponseBase.success(
            result={**result, "current": current, "pageSize": pageSize}
        )
