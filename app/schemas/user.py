# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:46
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import Optional

from pydantic import BaseModel


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
        orm_mode = True


class AddUserModel(UserModel):
    """
    新增用户模型
    """
    role_id: Optional[str]
    post_id: Optional[str]
    type: Optional[str]


class AddUser(BaseModel):

    username: Optional[str]
    nickname: Optional[str]
    password: Optional[str]
    created_by: Optional[int]
    updated_by: Optional[int]
