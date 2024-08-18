# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/12 16:38
@Author   : wiesZheng
@Software : PyCharm
"""

from fastapi.security import HTTPAuthorizationCredentials
from typing_extensions import Annotated

from app.commons.response.response_code import CustomErrorCode
from app.core.security import Jwt

from app.core.security.Jwt import create_access_token, DependsJwtAuth

from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.core.security.password import verify_psw
from app.crud.auth.user import UserCRUD
from app.exceptions.errors import CustomException
from app.schemas.auth.user import (
    RegisterUserParam,
    AuthLoginParam,
    GetCurrentUserInfoDetail,
    GetUserInfoNoRelationDetail,
)


class UserService:

    @staticmethod
    async def register_user(user_item: RegisterUserParam) -> ResponseModel:
        """用户注册"""
        current_user = await UserCRUD.user_add(user_item)
        access_token = await create_access_token(current_user.id)
        data = GetUserInfoNoRelationDetail.model_validate(current_user).model_dump()
        result = {"data": data, "access_token": access_token, "token_type": "Bearer"}
        return await ResponseBase.success(result=result)

    @staticmethod
    async def get_current_user_info(
        credentials: Annotated[HTTPAuthorizationCredentials, DependsJwtAuth]
    ) -> ResponseModel:
        # token = request.headers.get('Authorization')
        # if not token:
        #     return
        # scheme, token = get_authorization_scheme_param(token)
        if credentials.scheme.lower() != "bearer":
            return await ResponseBase.fail()

        sub = await Jwt.decode_jwt_token(credentials.credentials)
        current_user = await Jwt.get_current_user(sub)
        data = GetCurrentUserInfoDetail.model_validate(current_user).model_dump()

        return await ResponseBase.success(result=data)

    @staticmethod
    async def login(params: AuthLoginParam) -> ResponseModel:
        """
        登录
        :return:
        """
        username = params.username
        password = params.password
        if not username and not password:
            raise CustomException(CustomErrorCode.PARTNER_CODE_PARAMS_FAIL)
        current_user = await UserCRUD.get(username=username)
        if not current_user:
            raise CustomException(CustomErrorCode.WRONG_USER_NAME_OR_PASSWORD)
        elif not await verify_psw(password, current_user["password"]):
            raise CustomException(CustomErrorCode.WRONG_USER_NAME_OR_PASSWORD)
        elif current_user["is_valid"]:
            raise CustomException(CustomErrorCode.USER_ACCOUNT_LOCKED)

        access_token = await create_access_token(current_user["id"])
        await UserCRUD.update_login_time(current_user["id"])
        data = GetUserInfoNoRelationDetail.model_validate(current_user).model_dump()
        result = {
            "data": data,
            "access_token": access_token,
            "token_type": "Bearer",
        }
        return await ResponseBase.success(result=result)
