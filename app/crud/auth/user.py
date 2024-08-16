# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 17:36
@Author   : wiesZheng
@Software : PyCharm
"""
from datetime import datetime, timezone

from fastapi import Depends
from pydantic import BaseModel

from app.commons.response.response_code import CustomErrorCode
from app.core.security.Jwt import oauth2_scheme, decode_jwt_token
from app.crud import BaseCRUD
from app.exceptions.exception import BusinessException
from app.models.user import UserModel
from app.schemas.auth.user import RegisterUserParam


class UserCRUD(BaseCRUD):
    __model__ = UserModel

    # @classmethod
    # async def authenticate_user(
    #         cls,
    #         login_form: CustomOAuth2PasswordRequestForm,
    # ) -> UserModel:
    #
    #
    #     user = await UserCRUD(auth).get_by_username(login_form.username)
    #     if not verify_password(login_form.password, user.password):
    #         raise BusinessException(ErrorCodeEnum.ACCOUNT_ERR)
    #
    #     if not user.available:
    #         raise BusinessException(ErrorCodeEnum.ACCOUNT_ERR)
    #
    #     return user

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
    async def verify_user_register_info(cls, user_item: RegisterUserParam):
        """ 校验用户注册信息 """
        # 校验用户名是否存在
        result = await cls.exists(username=user_item.username)
        if result:
            raise ValueError(CustomErrorCode.USERNAME_OR_EMAIL_IS_REGISTER.msg)
        # 校验邮箱是否存在
        result = await cls.exists(email=user_item.email)
        if result:
            raise ValueError(CustomErrorCode.USER_EMAIL_OR_EMAIL_IS_REGISTER.msg)

    @classmethod
    async def user_add(cls, user_item: RegisterUserParam):
        await cls.verify_user_register_info(user_item)
        user = await cls.create(obj=user_item)
        # 创建注册用户
        if await cls.count() == 1:
            user = await cls.update_user_role(user_id=user["id"])
        current_user = user.to_dict("password")
        return current_user

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)):
        """
        根据token获取当前用户信息
        """

        if token.startswith('Bearer'):
            token = token.split(' ')[1]
        payload = await decode_jwt_token(token)
        user_id: str = payload.get("id")

        user_info = await cls.get(id=user_id)
        return user_info
