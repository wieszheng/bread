# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/12 16:38
@Author   : wiesZheng
@Software : PyCharm
"""

from fastapi import Request, Depends

from fastapi.security import OAuth2PasswordRequestForm

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import Success
from app.core.security.Jwt import create_access_token, decrypt_rsa_password, encrypt_rsa_password

from app.exceptions.exception import BusinessException

from app.commons.response.response_schema import unified_resp
from app.crud.auth.user import UserCRUD
from app.schemas.auth.user import RegisterUserParam, UserLogin, UserTokenIn, UserIn, AuthLoginParam


class UserService:

    @classmethod
    @unified_resp
    async def register_user(cls, user_item: RegisterUserParam):
        """用户注册"""
        user_item.password = await encrypt_rsa_password(user_item.password)
        user = await UserCRUD.user_add(user_item)
        access_token = await create_access_token(user)
        return {'user_info': user, 'access_token': access_token, 'token_type': 'Bearer'}

    @classmethod
    @unified_resp
    async def get_current_user_info(cls, token: str = Depends(UserCRUD.get_current_user)):
        return token

    @staticmethod
    @unified_resp
    async def login(params: AuthLoginParam):
        """
        登录
        :return:
        """
        username = params.username
        password = params.password
        if not username and not password:
            raise ValueError(CustomErrorCode.PARTNER_CODE_PARAMS_FAIL.msg)
        user_info = await UserCRUD.get(username=username)
        if not user_info:
            raise ValueError(CustomErrorCode.WRONG_USER_NAME_OR_PASSWORD.msg)
        u_password = await decrypt_rsa_password(user_info["password"])
        if u_password != password:
            raise ValueError(CustomErrorCode.WRONG_USER_NAME_OR_PASSWORD.msg)

        access_token = await create_access_token(user_info["id"])
        await UserCRUD.update_login_time(user_info["id"])

        token_user_info = UserTokenIn.model_validate({"data": user_info,
                                                      'access_token': access_token,
                                                      'token_type': 'Bearer'})

        return token_user_info.model_dump()
