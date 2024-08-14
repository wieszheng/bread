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

from app.schemas.resp import ResponseBaseModel


class UserModel(BaseModel):
    """
    用户表对应pydantic模型
    """
    user_id: Optional[int]
    dept_id: Optional[int]
    user_name: Optional[str]
    nick_name: Optional[str]
    user_type: Optional[str]
    email: Optional[str]
    phonenumber: Optional[str]
    sex: Optional[str]
    avatar: Optional[str]
    password: Optional[str]
    status: Optional[str]
    del_flag: Optional[str]
    login_ip: Optional[str]
    login_date: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]
    remark: Optional[str]

    class Config:
        from_attributes = True


class UserRegisterIn(BaseModel):
    """ 用户注册入参 """
    username: str = Field(..., title="用户名", description="必传")
    password: str = Field(..., title="密码", description="必传")
    nickname: str = Field(..., title="姓名", description="必传")
    email: EmailStr = Field(..., title="邮箱号", examples=["user@qq.com"], description="必传")

    @field_validator("username")
    def validate_username(cls, value: str):
        if len(value) < 4:
            raise ValueError("用户名长度不能小于4")
        return value

    @field_validator("email")
    def validate_email(cls, value: str):
        if not value.endswith("@qq.com"):
            raise ValueError("邮箱格式不正确")
        return value


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLoginIn(BaseModel):
    username: str
    password: str


class AddUser(UserRegisterIn):
    role: Optional[int] = Field(None, title="用户权限", description="可选填")
    last_login_at: datetime = Field(..., title="登录时间", description="必传")


class CurrentUserInfo(BaseModel):
    """
    数据库返回当前用户信息
    """
    username: Optional[str]
    nickname: Optional[str]
    password: Optional[str]


class UserRegisterOut(ResponseBaseModel):
    result: Union[Token, AddUser]
