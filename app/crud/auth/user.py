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

user_crud = BaseCRUD(SysUser)


class UserCRUD:
    @staticmethod
    async def add_user(user: AddUser):
        return await user_crud.create(obj=user)
