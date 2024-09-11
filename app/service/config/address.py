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
from app.crud.config.address import AddressCRUD
from app.crud.config.environment import EnvironmentCRUD
from app.exceptions.errors import CustomException
from app.schemas.auth.user import CurrentUserInfo
from app.schemas.config.address import AddressSchemaBase, UpdateAddressParam


class AddressService:
    @staticmethod
    async def create_address(
        obj: AddressSchemaBase,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_env_id = await EnvironmentCRUD.exists(id=obj.env, is_deleted=False)
        if not input_env_id:
            raise CustomException(CustomErrorCode.ENVIRONMENT_ID_NOT_EXIST)
        input_address_name = await AddressCRUD.exists(name=obj.name, is_deleted=False)
        if input_address_name:
            raise CustomException(CustomErrorCode.ADDRESS_NAME_EXIST)
        result = await AddressCRUD.create(obj=obj, created_by=user_info.id)
        return await ResponseBase.success(result=result.to_dict())

    @staticmethod
    async def get_address(address_id: Annotated[int, ...]) -> ResponseModel:
        input_address_id = await AddressCRUD.exists(id=address_id, is_deleted=False)
        if not input_address_id:
            raise CustomException(CustomErrorCode.ADDRESS_ID_NOT_EXIST)
        result = await AddressCRUD.get(id=address_id)
        return await ResponseBase.success(result=result)

    @staticmethod
    async def delete_address(address_id: Annotated[int, ...]) -> ResponseModel:
        input_address_id = await AddressCRUD.exists(id=address_id)
        if not input_address_id:
            raise CustomException(CustomErrorCode.ADDRESS_ID_NOT_EXIST)
        await AddressCRUD.delete(id=address_id)
        return await ResponseBase.success()

    @staticmethod
    async def update_address(
        obj: UpdateAddressParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_address_id = await AddressCRUD.exists(id=obj.id, is_deleted=False)
        if not input_address_id:
            raise CustomException(CustomErrorCode.ADDRESS_ID_NOT_EXIST)
        input_env_id = await EnvironmentCRUD.exists(id=obj.env, is_deleted=False)
        if not input_env_id:
            raise CustomException(CustomErrorCode.ENVIRONMENT_ID_NOT_EXIST)
        await AddressCRUD.update(
            obj={**obj.model_dump(), "updated_by": user_info.id}, id=obj.id
        )
        return await ResponseBase.success()

    @staticmethod
    async def get_address_list(
        current: Annotated[int, Query(...)] = 1,
        pageSize: Annotated[int, Query(...)] = 10,
        env: Annotated[int | None, Query(description="环境ID")] = None,
        name: Annotated[str | None, Query(description="网关名称")] = None,
    ) -> ResponseModel:
        result = await AddressCRUD.get_list(
            limit=pageSize,
            offset=current,
            name=name,
            env=env,
        )

        return await ResponseBase.success(
            result={**result, "current": current, "pageSize": pageSize}
        )
