# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:55
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter, Depends

from app.core.security.Jwt import DependsJwtAuth
from app.core.security.permission import RequestPermission
from app.service.auth.user import UserService
from config import settings

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
    "/{username}",
    endpoint=UserService.get_user,
    response_model_exclude={"result": {"password"}},
    dependencies=[DependsJwtAuth],
    methods=["get"],
    summary="查看用户信息",
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
    endpoint=UserService.update_user,
    methods=["put"],
    summary="更新用户信息",
    dependencies=[Depends(RequestPermission(settings.MEMBER)), DependsJwtAuth],
)

router.add_api_route(
    "",
    endpoint=UserService.get_pagination_users,
    methods=["post"],
    summary="（支持条件）分页获取所有用户",
)

router.add_api_route(
    "/{userId}",
    endpoint=UserService.delete_user,
    methods=["delete"],
    summary="用户注销",
    description="用户注销 != 用户登出，注销之后用户将从数据库逻辑删除",
    dependencies=[Depends(RequestPermission(settings.ADMIN)), DependsJwtAuth],
)
