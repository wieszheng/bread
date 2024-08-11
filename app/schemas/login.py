#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/11 23:54
@Author   : wiesZheng
@Software : PyCharm
"""
from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str = Field(description='用户名称')
    password: str = Field(description='用户密码')
