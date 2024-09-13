# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 17:36
@Author   : wiesZheng
@Software : PyCharm
"""

import asyncio
from datetime import datetime

from app.commons.response.response_code import CustomErrorCode
from app.core.security.password import hash_psw
from app.crud import BaseCRUD
from app.exceptions.errors import CustomException
from app.models.user import User
from app.schemas.auth.user import RegisterUserParam


class UserCRUD(BaseCRUD):
    __model__ = User

    @classmethod
    async def update_user_role(cls, user_id: int, role: int = 2):
        res = await cls.exists(id=user_id)
        if res:
            await cls.update(obj={'role': role}, id=user_id)

    @classmethod
    async def update_login_time(cls, user_id: int):
        res = await cls.exists(id=user_id)
        if res:
            return await cls.update(obj={'last_login_at': datetime.now()}, id=user_id)

    @classmethod
    async def user_add(cls, user_item: RegisterUserParam):
        # 校验用户名、邮箱是否存在
        result_name, result_email = await asyncio.gather(
            cls.exists(username=user_item.username), cls.exists(email=user_item.email)
        )
        if result_name:
            raise CustomException(CustomErrorCode.USERNAME_OR_EMAIL_IS_REGISTER)
        if result_email:
            raise CustomException(CustomErrorCode.USER_EMAIL_OR_EMAIL_IS_REGISTER)

        user_item.password = await hash_psw(user_item.password)
        # 创建注册用户
        if await cls.count() == 0:
            current_user = await cls.create(obj=user_item, role=2)
        else:
            current_user = await cls.create(obj=user_item)
        return current_user

    @classmethod
    async def reset_password(cls, user_id: int, new_password: str):
        await cls.update(obj={'password': await hash_psw(new_password)}, id=user_id)
        return ''
