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
from app.models.environment import Environment
from app.models.user import User
from app.schemas.auth.user import UserInfoSchemaBase


class EnvironmentCRUD(BaseCRUD):
    __model__ = Environment

    @classmethod
    async def get_list(
        cls,
        limit: int = 10,
        offset: int = 1,
        filter_params: dict = None,
        orderings: str = None,
    ):
        if not orderings:
            orderings = "id"
        if not filter_params:
            filter_params = {}

        return await cls.get_multi_joined(
            limit=limit,
            offset=compute_offset(offset, limit),
            sort_columns=orderings,
            sort_orders="desc",
            joins_config=[
                JoinConfig(
                    model=User,
                    join_on=cls.__model__.created_by == User.id,
                    join_prefix="user_",
                    schema_to_select=UserInfoSchemaBase,
                    join_type="left",
                ),
            ],
            **filter_params
        )
