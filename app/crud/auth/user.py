# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 17:36
@Author   : wiesZheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.enums.exception import ErrorCodeEnum
from app.exceptions.exception import BusinessException
from app.models.user import SysUser
from app.schemas.user import AddUser, UserRegisterIn


class UserCRUD(BaseCRUD):
    __model__ = SysUser

    @classmethod
    async def verify_user_register_info(cls, user_item: UserRegisterIn):
        """ 校验用户注册信息 """
        # 校验用户名是否存在
        result = await cls.exists(username=user_item.username)
        if result:
            raise BusinessException(ErrorCodeEnum.ACCOUNT_ERR)

        # 校验手机号是否存在
        result = await cls.exists(phone=user_item.phone)
        if result:
            raise BusinessException(ErrorCodeEnum.MOBILE_ERR)

    @classmethod
    async def user_add(cls, user_item: UserRegisterIn):
        await cls.verify_user_register_info(user_item)
        # 创建注册用户
        user = await cls.create(obj=user_item)
        current_user = user.to_dict("password")

        return current_user
