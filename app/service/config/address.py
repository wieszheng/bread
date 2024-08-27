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
from app.crud.config.address import AddressCRUD
from app.crud.config.environment import EnvironmentCRUD
from app.exceptions.errors import CustomException
from app.schemas.config.address import AddressSchemaBase, UpdateAddressParam


class AddressService:
    @staticmethod
    async def create_address(request: Request, obj: AddressSchemaBase) -> ResponseModel:
        input_env_id = await EnvironmentCRUD.exists(id=obj.env)
        # if not input_env_id:
        #     raise CustomException(CustomErrorCode.ENVIRONMENT_ID_NOT_EXIST)
        input_address_name = await AddressCRUD.exists(name=obj.name)
        if input_address_name:
            raise CustomException(CustomErrorCode.ADDRESS_NAME_EXIST)
        result = await AddressCRUD.create(obj=obj, created_by=request.user.id)
        return await ResponseBase.success(result=result.to_dict())

    @staticmethod
    async def get_address(address_id: Annotated[int, ...]) -> ResponseModel:
        input_address_id = await AddressCRUD.exists(id=address_id)
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
        request: Request, obj: UpdateAddressParam
    ) -> ResponseModel:
        input_address_id = await AddressCRUD.exists(id=obj.id)
        if not input_address_id:
            raise CustomException(CustomErrorCode.ADDRESS_ID_NOT_EXIST)
        await AddressCRUD.update(
            obj={**obj.model_dump(), "updated_by": request.user.id}, id=obj.id
        )
        return await ResponseBase.success()

    @staticmethod
    async def get_address_list(obj) -> ResponseModel:
        return await ResponseBase.success()
