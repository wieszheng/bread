# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:46
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import Optional

from pydantic import BaseModel, Field, field_validator


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
    username: str = Field(..., min_length=3, max_length=50, description='用户名')
    nickname: str = Field(..., min_length=2, max_length=50, description='用户昵称')
    phone: str = Field(..., min_length=11, description='用户手机号')
    password: str = Field(..., min_length=6, max_length=50, description='用户密码')


class AddUser(BaseModel):
    username: Optional[str]
    nickname: Optional[str]
    password: Optional[str]


class CurrentUserInfo(BaseModel):
    """
    数据库返回当前用户信息
    """
    username: Optional[str]
    nickname: Optional[str]
    password: Optional[str]
