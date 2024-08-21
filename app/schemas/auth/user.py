# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:46
@Author   : wiesZheng
@Software : PyCharm
"""
from datetime import datetime
from typing import Optional, Any

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    EmailStr,
    ConfigDict,
    HttpUrl,
    field_serializer,
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
    captcha: str = None


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
    email: EmailStr = Field(..., example="user@example.com")
    phone: CustomPhoneNumber | None = None


class GetUserInfoNoRelationDetail(UserInfoSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    avatar: str | None = None
    role: RoleType = Field(default=RoleType.MEMBER)
    is_valid: bool
    last_login_at: datetime | None = None

    @field_serializer("last_login_at")
    def serialize_dt(self, last_login_at: datetime | None, _info: Any) -> str | None:
        if last_login_at is not None:
            return last_login_at.strftime("%Y-%m-%d %H:%M:%S")

        return None


class GetCurrentUserInfoDetail(GetUserInfoNoRelationDetail):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime


class GetUserInfoNoRelationDetail(GetUserInfoNoRelationDetail):
    model_config = ConfigDict(from_attributes=True)


class GetUserInfoListDetails(GetUserInfoNoRelationDetail):
    model_config = ConfigDict(from_attributes=True)


class CurrentUserIns(GetUserInfoListDetails):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime | None = None
    updated_at: datetime | None = None
    created_by: int | None = None


class ResetPasswordParam(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str


class UpdateUserParam(UserInfoSchemaBase):
    pass


class AvatarParam(BaseModel):
    url: HttpUrl = Field(..., description="头像 http 地址")


class RentalDemandListQuery(BaseModel):
    username: Optional[str] = Field(default=None, description="用户账号")
    nickname: Optional[str] = Field(default=None, description="用户昵称")


class UserRentalDemandListIn(ListPageRequestModel):
    query_params: Optional[RentalDemandListQuery] = Field(
        default={}, description="查询参数"
    )
