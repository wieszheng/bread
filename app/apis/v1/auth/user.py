# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:55
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter, Depends

from app.commons.resq import unified_resp
from app.crud.auth.user import UserCRUD
from app.crud.auth.login import LoginCRUD
from app.schemas.user import AddUser

router = APIRouter(prefix="/system/user", tags=["用户接口"])


@router.post("/me", summary="用户")
@unified_resp
async def login(token: str = Depends(LoginCRUD.get_current_user)):
    return token


@router.post("/add", summary="添加用户")
@unified_resp
async def create_user(user: AddUser):
    data = await UserCRUD.add_user(user)

    return data.to_dict()
