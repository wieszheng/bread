# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:46
@Author   : wiesZheng
@Software : PyCharm
"""
from datetime import datetime
from typing import Any, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    field_serializer,
    field_validator,
)
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.commons.enums import RoleType
from app.commons.response.response_schema import ListPageRequestModel


class AuthSchemaBase(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

    @field_validator("username")
    def validate_username(cls, value: str):
        if len(value) < 4:
            raise ValueError("用户名长度不能小于4")
        return value


class AuthLoginParam(AuthSchemaBase):
    pass


class RegisterUserParam(AuthSchemaBase):
    """用户注册入参"""

    nickname: str = Field(..., title="姓名", description="必传")
    email: EmailStr = Field(
        ..., title="邮箱号", examples=["user@qq.com"], description="必传"
    )

    @field_validator("email")
    def validate_email(cls, value: str):
        if not value.endswith("@qq.com"):
            raise ValueError("邮箱格式不正确")
        return value


class CustomPhoneNumber(PhoneNumber):
    default_region_code = "CN"


class UserInfoSchemaBase(BaseModel):
    username: str
    nickname: str
    email: EmailStr = Field(..., example="user@qq.com")
    phone: CustomPhoneNumber | None = None
    avatar: str | None = None


class GetUserInfoNoRelationDetail(UserInfoSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: RoleType = Field(default=RoleType.MEMBER)
    is_valid: bool
    last_login_at: datetime | None = None


class CurrentUserInfo(BaseModel):
    id: int
    username: str
    nickname: str
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    role: RoleType
    is_valid: bool
    last_login_at: datetime | None = None


class CurrentUserIns(GetUserInfoNoRelationDetail):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime | None = None
    updated_at: datetime | None = None
    created_by: int | None = None


class ResetPasswordParam(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str


class UpdateUserParam(BaseModel):
    id: int
    nickname: str = None
    email: EmailStr = Field(..., example="user@qq.com")
    phone: CustomPhoneNumber | None = None


class AvatarParam(BaseModel):
    url: HttpUrl = Field(..., description="头像 http 地址")


class UpdateUserControlParam(BaseModel):
    id: int = Field(description="用户id")
    is_valid: bool = Field(default=False, description="是否激活")


class UpdateUserRoleParam(BaseModel):
    id: int = Field(description="用户id")
    role: int = Field(description="用户权限")
    username: str = None
    email: EmailStr = Field(example="user@qq.com")
