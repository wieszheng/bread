# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/12 16:38
@Author   : wiesZheng
@Software : PyCharm
"""

import uuid

from fastapi import Depends, File, Path, Query, UploadFile
from typing_extensions import Annotated

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.core.client.miNio import minio_client
from app.core.security.Jwt import create_access_token, get_current_user_new
from app.core.security.password import verify_psw
from app.crud.auth.user import UserCRUD
from app.crud.helper import compute_offset
from app.exceptions.errors import CustomException, PermissionException
from app.schemas.auth.user import (
    AuthLoginParam,
    CurrentUserInfo,
    CurrentUserIns,
    GetUserInfoNoRelationDetail,
    RegisterUserParam,
    ResetPasswordParam,
    UpdateUserControlParam,
    UpdateUserParam,
    UpdateUserRoleParam,
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

    @staticmethod
    async def get_current_user_info(
        user_info: CurrentUserInfo = Depends(get_current_user_new),
    ) -> ResponseModel:
        """
        个人信息
        returns the current user
        """
        return await ResponseBase.success(result=user_info.model_dump())

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
        result = {
            "access_token": access_token,
            "token_type": "Bearer",
        }
        return await ResponseBase.success(result=result)

    @staticmethod
    async def password_reset(
        obj: ResetPasswordParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        """
        重置密码
        :return:
        """
        if obj.new_password == obj.old_password:
            raise CustomException(CustomErrorCode.NEW_PWD_NO_OLD_PWD_EQUAL)

        current_user = await UserCRUD.get(id=user_info.id)
        if not await verify_psw(obj.old_password, current_user["password"]):
            raise CustomException(CustomErrorCode.OLD_PASSWORD_ERROR)

        np1 = obj.new_password
        np2 = obj.confirm_password
        if np1 != np2:
            raise CustomException(CustomErrorCode.PASSWORD_TWICE_IS_NOT_AGREEMENT)

        await UserCRUD.reset_password(user_info.id, obj.new_password)
        return await ResponseBase.success()

    @staticmethod
    async def update_avatar(
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
        avatar: Annotated[UploadFile, File(..., description="上传的头像文件")],
    ) -> ResponseModel:
        """
        更新头像
        :return:
        """
        random_suffix = str(uuid.uuid4()).replace("-", "")
        object_name = f"{user_info.id}/{random_suffix}.{avatar.filename.split('.')[-1]}"
        minio_client.upload_file(
            object_name, avatar.file, content_type=avatar.content_type
        )

        avatar_url = minio_client.pre_signature_get_object_url(object_name)
        await UserCRUD.update(
            obj={"avatar": avatar_url.split("?", 1)[0], "updated_by": user_info.id},
            id=user_info.id,
        )
        return await ResponseBase.success(
            result={"avatar": avatar_url.split("?", 1)[0]}
        )

    @staticmethod
    async def get_pagination_users(
        current: Annotated[int, Query(...)] = 1,
        pageSize: Annotated[int, Query(...)] = 10,
        nickname: Annotated[str | None, Query(description="用户昵称")] = None,
        id: Annotated[int | None, Query(description="用户ID")] = None,
    ) -> ResponseModel:
        """
        分页查询用户
        :return:
        """
        filter_params = {}
        if nickname or id:
            filter_params = {"nickname": nickname, "id": id}

        result = await UserCRUD.get_multi(
            limit=pageSize,
            offset=compute_offset(current, pageSize),
            is_deleted=False,
            schema_to_select=CurrentUserIns,
            # return_as_model=True,
            # sort_columns='username',
            # sort_orders='desc',
            **filter_params,
        )

        return await ResponseBase.success(
            result={**result, "current": current, "pageSize": pageSize}
        )

    @staticmethod
    async def delete_user(
        userId: Annotated[int, Path(...)],
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        """
        删除用户
        :return:
        """
        if user_info.role < 2:
            if user_info.id != userId:
                raise PermissionException("不可操作,暂无权限！")
        elif user_info.id == userId:
            raise PermissionException("不可操作管理员信息！")

        input_user = await UserCRUD.exists(id=userId)
        if not input_user:
            raise CustomException(CustomErrorCode.PARTNER_CODE_TOKEN_EXPIRED_FAIL)
        await UserCRUD.delete(id=userId)

        return await ResponseBase.success()

    @staticmethod
    async def get_user(userId: Annotated[int, Path(...)]) -> ResponseModel:
        """
        获取用户
        :return:
        """
        input_user = await UserCRUD.get(id=userId)
        return await ResponseBase.success(result=input_user)

    @staticmethod
    async def update_user(
        obj: UpdateUserParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        """
        更新用户
        :return:
        """
        input_user = await UserCRUD.get(id=obj.id)
        if not input_user:
            raise CustomException(CustomErrorCode.PARTNER_CODE_TOKEN_EXPIRED_FAIL)
        if user_info.role < 2:
            if user_info.id != obj.id:
                raise CustomException(CustomErrorCode.YOU_INFO)
        elif input_user["role"] == 2:
            raise CustomException(CustomErrorCode.USER_IS_ADMIN)

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

    @staticmethod
    async def is_valid(
        obj: UpdateUserControlParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        result = await UserCRUD.get(id=obj.id)
        if not result:
            raise CustomException(CustomErrorCode.PARTNER_CODE_TOKEN_EXPIRED_FAIL)
        if result["role"] == 2:
            if user_info.id != obj.id or user_info.id == obj.id:
                raise PermissionException("不可操作其他管理员信息,警告！")

        await UserCRUD.update(
            obj={**obj.model_dump(), "updated_by": user_info.id}, id=obj.id
        )
        return await ResponseBase.success()

    @staticmethod
    async def update_user_role(
        obj: UpdateUserRoleParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        result = await UserCRUD.get(id=obj.id)
        if not result:
            raise CustomException(CustomErrorCode.PARTNER_CODE_TOKEN_EXPIRED_FAIL)
        if result["role"] == 2:
            if user_info.id != obj.id or user_info.id == obj.id:
                raise PermissionException("不可操作其他管理员信息,警告！")
        await UserCRUD.update(
            obj={**obj.model_dump(), "updated_by": user_info.id}, id=obj.id
        )
        return await ResponseBase.success()
