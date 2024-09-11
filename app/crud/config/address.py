# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 14:53
@Author   : wiesZheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.crud.helper import JoinConfig, compute_offset
from app.models.address import Address
from app.models.environment import Environment
from app.models.user import User
from app.schemas.auth.user import UserInfoSchemaBase
from app.schemas.config.environment import EnvironmentSchemaBase


class AddressCRUD(BaseCRUD):
    __model__ = Address

    @classmethod
    async def get_list(
        cls, limit: int = 10, offset: int = 1, name: str = None, env: int = None
    ):
        filter_params = {}
        if name or env:
            filter_params = {"name": name, "env": env}

        return await cls.get_multi_joined(
            limit=limit,
            offset=compute_offset(offset, limit),
            joins_config=[
                JoinConfig(
                    model=User,
                    join_on=cls.__model__.created_by == User.id,
                    join_prefix="user_",
                    schema_to_select=UserInfoSchemaBase,
                    join_type="left",
                ),
                JoinConfig(
                    model=Environment,
                    join_on=cls.__model__.env == Environment.id,
                    join_prefix="env_",
                    schema_to_select=EnvironmentSchemaBase,
                    join_type="left",
                ),
            ],
            is_deleted=False,
            **filter_params,
        )
