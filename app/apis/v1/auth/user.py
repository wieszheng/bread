# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:55
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter, Depends

from app.commons.response.response_schema import ResponseModel
from app.core.security.Jwt import DependsJwtAuth
from app.core.security.permission import RequestPermission
from app.service.auth.user import UserService

router = APIRouter(prefix="/system/user", tags=["用户接口"])

router.add_api_route(
    "/login",
    endpoint=UserService.login,
    methods=["post"],
    summary="用户登录",
)

router.add_api_route(
    "/me",
    endpoint=UserService.get_current_user_info,
    dependencies=[DependsJwtAuth],
    methods=["get"],
    summary="获取当前用户信息",
)

router.add_api_route(
    "/register",
    endpoint=UserService.register_user,
    methods=["post"],
    summary="注册用户",
)

router.add_api_route(
    "/password/reset",
    endpoint=UserService.password_reset,
    dependencies=[DependsJwtAuth],
    methods=["post"],
    summary="密码重置",
)

router.add_api_route(
    "/{username}/avatar",
    endpoint=UserService.update_avatar,
    dependencies=[DependsJwtAuth],
    methods=["put"],
    summary="更新头像",
)

router.add_api_route(
    "/{username}",
    endpoint=UserService.register_user,
    methods=["put"],
    summary="更新用户信息",
)

router.add_api_route(
    "",
    endpoint=UserService.get_pagination_users,
    methods=["post"],
    summary="（模糊条件）分页获取所有用户",
)

router.add_api_route(
    "/{username}",
    endpoint=UserService.register_user,
    methods=["delete"],
    summary="用户注销",
)
