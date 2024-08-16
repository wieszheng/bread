# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:46
@Author   : wiesZheng
@Software : PyCharm
"""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator, EmailStr


class AuthSchemaBase(BaseModel):
    username: str = Field(..., description='用户名')
    password: str = Field(..., description='密码')

    @field_validator("username")
    def validate_username(cls, value: str):
        if len(value) < 4:
            raise ValueError("用户名长度不能小于4")
        return value


class AuthLoginParam(AuthSchemaBase):
    captcha: str = None


class RegisterUserParam(AuthSchemaBase):
    """ 用户注册入参 """

    nickname: str = Field(..., title="姓名", description="必传")
    email: EmailStr = Field(..., title="邮箱号", examples=["user@qq.com"], description="必传")

    @field_validator("email")
    def validate_email(cls, value: str):
        if not value.endswith("@qq.com"):
            raise ValueError("邮箱格式不正确")
        return value


class UserLogin(BaseModel):
    username: str = Field(..., description='用户名')
    password: str = Field(..., description='密码')


class UserIn(BaseModel):
    id: int = Field(None, description='id')
    avatar: Optional[str] = Field(None, description='头像')
    username: str = Field(None, description='用户名称')
    nickname: str = Field(None, description='用户昵称')
    role: int = Field(None, description='权限')
    last_login_at: Optional[datetime] = Field(None, description='登录时间')


class UserTokenIn(BaseModel):
    """
    用户登录返回信息
    """
    data: UserIn
    access_token: str = Field(None, description='令牌token')
    token_type: str = Field(None, description='令牌类型')


class UserLoginIn(BaseModel):
    username: str
    password: str


class CurrentUserInfo(BaseModel):
    """
    数据库返回当前用户信息
    """
    username: Optional[str]
    nickname: Optional[str]
    password: Optional[str]
