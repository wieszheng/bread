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

from app.commons.resq import Success
from app.core.security import create_access_token
from app.enums.exception import StatusCodeEnum
from app.exceptions.exception import BusinessException

from app.commons.resq import unified_resp
from app.crud.auth.user import UserCRUD
from app.schemas.user import UserRegisterIn


class UserService:

    @classmethod
    @unified_resp
    async def register_user(cls, user_item: UserRegisterIn):
        user = await UserCRUD.user_add(user_item)
        access_token = await create_access_token(user)
        return {'user_info': user, 'access_token': access_token, 'token_type': 'Bearer'}

    @classmethod
    @unified_resp
    async def get_current_user_info(cls, token: str = Depends(UserCRUD.get_current_user)):
        return token

    @classmethod
    async def login(cls, request: Request, form_data: OAuth2PasswordRequestForm = Depends()):

        user = await UserCRUD.get(username=form_data.username, password=form_data.password)
        if user is None:
            raise BusinessException(StatusCodeEnum.USER_ERR)
        access_token = await create_access_token(UserCRUD.__model__(**user).to_dict("password"))
        request_from_swagger = request.headers.get('referer').endswith('docs') if request.headers.get(
            'referer') else False
        request_from_redoc = request.headers.get('referer').endswith('redoc') if request.headers.get(
            'referer') else False
        if request_from_swagger or request_from_redoc:
            return {'access_token': access_token, 'token_type': 'Bearer'}
        return Success(
            result={'access_token': access_token, 'token_type': 'Bearer'},
            message='登录成功'
        )
