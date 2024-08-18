# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 17:36
@Author   : wiesZheng
@Software : PyCharm
"""
from datetime import datetime

from app.commons.response.response_code import CustomErrorCode

from app.core.security.password import hash_psw
from app.crud import BaseCRUD
from app.exceptions.errors import CustomException
from app.models.user import UserModel
from app.schemas.auth.user import RegisterUserParam


class UserCRUD(BaseCRUD):
    __model__ = UserModel

    @classmethod
    async def update_user_role(cls, user_id: int, role: int = 2):
        res = await cls.exists(id=user_id)
        if res:
            await cls.update(obj={"role": role}, id=user_id)

    @classmethod
    async def update_login_time(cls, user_id: int):
        res = await cls.exists(id=user_id)
        if res:
            return await cls.update(obj={"last_login_at": datetime.now()}, id=user_id)

    @classmethod
    async def user_add(cls, user_item: RegisterUserParam):
        # 校验用户名是否存在
        result = await cls.exists(username=user_item.username)
        if result:
            raise CustomException(CustomErrorCode.USERNAME_OR_EMAIL_IS_REGISTER)
        # 校验邮箱是否存在
        result = await cls.exists(email=user_item.email)
        if result:
            raise CustomException(CustomErrorCode.USER_EMAIL_OR_EMAIL_IS_REGISTER)

        user_item.password = await hash_psw(user_item.password)
        current_user = await cls.create(obj=user_item)
        # 创建注册用户
        if await cls.count() == 1:
            await cls.update_user_role(user_id=current_user.id)

        return current_user
