# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 17:36
@Author   : wiesZheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.models.user import SysUser
from app.schemas.user import AddUser


class UserCRUD(BaseCRUD):
    __model__ = SysUser

    @staticmethod
    async def add_user(user: AddUser):
        return await UserCRUD.create(obj=user)

    @staticmethod
    async def get_user_info(id: str):
        """
        获取用户信息
        :param id:
        :return:
        """
        data = await UserCRUD.get(id=id)
        return data
