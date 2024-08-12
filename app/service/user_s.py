# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/12 16:38
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import Depends

from app.commons.resq import unified_resp
from app.crud.auth.user import UserCRUD
from app.schemas.user import UserRegisterIn
from app.service.login_s import LoginService


class UserService:
    @classmethod
    @unified_resp
    async def get_current_user_info(cls, token: str = Depends(LoginService.get_current_user)):
        return token

    @classmethod
    # @unified_resp
    async def create_user(cls, user_item: UserRegisterIn):
        await UserCRUD.user_register(user_item)
