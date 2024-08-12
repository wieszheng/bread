# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:55
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter

from app.schemas.user import CurrentUserInfo
from app.service.user_s import UserService

router = APIRouter(prefix="/system/user", tags=["用户接口"])

router.add_api_route(
    "/me",
    endpoint=UserService.get_current_user_info,
    response_model=CurrentUserInfo,
    methods=["post"],
    summary="用户信息"
)

router.add_api_route(
    "/add",
    endpoint=UserService.create_user,
    methods=["post"],
    summary="添加用户"
)
