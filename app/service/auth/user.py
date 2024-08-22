# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/12 16:38
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import Path, Request
from typing_extensions import Annotated

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.core.security.Jwt import create_access_token
from app.core.security.password import verify_psw
from app.crud.auth.user import UserCRUD
from app.exceptions.errors import CustomException, PermissionException
from app.schemas.auth.user import (
    AuthLoginParam,
    AvatarParam,
    GetCurrentUserInfoDetail,
    GetUserInfoNoRelationDetail,
    RegisterUserParam,
    ResetPasswordParam,
    UpdateUserParam,
    UserRentalDemandListIn,
)


class UserService:

    @staticmethod
    async def register_user(obj: RegisterUserParam) -> ResponseModel:
        """
        用户注册
        return:
        """
        current_user = await UserCRUD.user_add(obj)
        access_token = await create_access_token(current_user.id)
        data = GetUserInfoNoRelationDetail.model_validate(current_user).model_dump()
        result = {"data": data, "access_token": access_token, "token_type": "Bearer"}
        return await ResponseBase.success(result=result)

    # @staticmethod
    # async def get_current_user_info(
    #         credentials: Annotated[HTTPAuthorizationCredentials, DependsJwtAuth]
    # ) -> ResponseModel:
    #     """
    #     个人信息
    #     returns the current user
    #     """
    #     # token = request.headers.get('Authorization')
    #     # if not token:
    #     #     return
    #     scheme, token = get_authorization_scheme_param(token)
    #     if credentials.scheme.lower() != "bearer":
    #         return await ResponseBase.fail()
    #
    #     sub = await Jwt.decode_jwt_token(credentials.credentials)
    #     current_user = await Jwt.get_current_user(sub)
    #     data = GetCurrentUserInfoDetail.model_validate(current_user).model_dump()
    #
    #     return await ResponseBase.success(result=data)
    @staticmethod
    async def get_current_user_info(request: Request) -> ResponseModel:
        """
        个人信息
        returns the current user
        """

        data = GetCurrentUserInfoDetail(**request.user.model_dump()).model_dump()
        return await ResponseBase.success(result=data)

    @staticmethod
    async def login(obj: AuthLoginParam) -> ResponseModel:
        """
        登录
        :return:
        """
        username = obj.username
        password = obj.password
        if not username and not password:
            raise CustomException(CustomErrorCode.PARTNER_CODE_PARAMS_FAIL)
        current_user = await UserCRUD.get(username=username)
        if not current_user:
            raise CustomException(CustomErrorCode.WRONG_USER_NAME_OR_PASSWORD)
        elif not await verify_psw(password, current_user["password"]):
            raise CustomException(CustomErrorCode.WRONG_USER_NAME_OR_PASSWORD)
        elif not current_user["is_valid"]:
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

    @staticmethod
    async def password_reset(
        request: Request, obj: ResetPasswordParam
    ) -> ResponseModel:
        """
        重置密码
        :return:
        """
        if obj.new_password == obj.old_password:
            raise CustomException(CustomErrorCode.NEW_PWD_NO_OLD_PWD_EQUAL)

        current_user = await UserCRUD.get(id=request.user.id)
        if not await verify_psw(obj.old_password, current_user["password"]):
            raise CustomException(CustomErrorCode.OLD_PASSWORD_ERROR)

        np1 = obj.new_password
        np2 = obj.confirm_password
        if np1 != np2:
            raise CustomException(CustomErrorCode.PASSWORD_TWICE_IS_NOT_AGREEMENT)

        await UserCRUD.reset_password(request.user.id, obj.new_password)
        return await ResponseBase.success()

    @staticmethod
    async def update_avatar(
        request: Request, username: Annotated[str, Path(...)], avatar: AvatarParam
    ) -> ResponseModel:
        """
        更新头像
        :return:
        """
        if request.user.role < 2:
            if request.user.username != username:
                raise PermissionException("不可操作,暂无权限！")
        input_user = await UserCRUD.exists(username=username)
        if not input_user:
            raise CustomException(CustomErrorCode.PARTNER_CODE_TOKEN_EXPIRED_FAIL)
        await UserCRUD.update_avatar(username, avatar)
        return await ResponseBase.success()

    @staticmethod
    async def get_pagination_users(obj: UserRentalDemandListIn) -> ResponseModel:
        """
        分页查询用户
        :return:
        """
        query_params = obj.query_params.dict() if obj.query_params else {}
        query_params = {k: v for k, v in query_params.items()}

        result = await UserCRUD.get_list(
            filter_params=query_params,
            orderings=obj.orderings,
            limit=obj.page_size,
            offset=obj.page,
            schema_to_select=GetUserInfoNoRelationDetail,
        )

        return await ResponseBase.success(
            result={**result, "page": obj.page, "page_size": obj.page_size}
        )

    @staticmethod
    async def delete_user(
        request: Request, userId: Annotated[int, Path(...)]
    ) -> ResponseModel:
        """
        删除用户
        :return:
        """
        if request.user.role < 2:
            if request.user.id != userId:
                raise PermissionException("不可操作,暂无权限！")
        elif request.user.id == userId:
            raise PermissionException("不可操作管理员信息！")

        input_user = await UserCRUD.exists(id=userId)
        if not input_user:
            raise CustomException(CustomErrorCode.PARTNER_CODE_TOKEN_EXPIRED_FAIL)
        await UserCRUD.delete(id=userId)

        return await ResponseBase.success()

    @staticmethod
    async def get_user(username: Annotated[str, Path(...)]) -> ResponseModel:
        """
        获取用户
        :return:
        """
        input_user = await UserCRUD.get(username=username)
        return await ResponseBase.success(result=input_user)

    @staticmethod
    async def update_user(
        request: Request,
        username: Annotated[str, Path(...)],
        obj: UpdateUserParam,
    ) -> ResponseModel:
        """
        更新用户
        :return:
        """
        if request.user.username != username:
            raise CustomException(CustomErrorCode.YOU_INFO)
        input_user = await UserCRUD.get(username=username)
        if not input_user:
            raise CustomException(CustomErrorCode.PARTNER_CODE_TOKEN_EXPIRED_FAIL)
        if input_user["username"] != obj.username:
            _username = await UserCRUD.get(username=obj.username)
            if _username:
                raise CustomException(CustomErrorCode.USERNAME_OR_EMAIL_IS_REGISTER)
        if input_user["nickname"] != obj.nickname:
            nickname = await UserCRUD.get(nickname=obj.nickname)
            if nickname:
                raise CustomException(CustomErrorCode.NICKNAME_OR_EMAIL_IS_REGISTER)
        if input_user["email"] != obj.email:
            email = await UserCRUD.get(email=obj.email)
            if email:
                raise CustomException(CustomErrorCode.USER_EMAIL_OR_EMAIL_IS_REGISTER)
        await UserCRUD.update(obj=obj, id=input_user["id"])
        return await ResponseBase.success()
