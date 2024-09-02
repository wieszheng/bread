# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 14:58
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter

from app.core.security.Jwt import DependsJwtAuth
from app.service.config.environment import EnvironmentService

router = APIRouter(prefix="/config/environment", tags=["环境配置"])

router.add_api_route(
    "",
    endpoint=EnvironmentService.create_environment,
    dependencies=[DependsJwtAuth],
    methods=["post"],
    summary="新增环境信息",
)

router.add_api_route(
    "",
    endpoint=EnvironmentService.get_environment,
    methods=["get"],
    summary="查询环境信息",
)

router.add_api_route(
    "",
    endpoint=EnvironmentService.delete_environment,
    dependencies=[DependsJwtAuth],
    methods=["delete"],
    summary="删除环境信息",
)

router.add_api_route(
    "",
    endpoint=EnvironmentService.update_environment,
    dependencies=[DependsJwtAuth],
    methods=["put"],
    summary="修改环境信息",
)

router.add_api_route(
    "/list",
    endpoint=EnvironmentService.get_environments,
    methods=["get"],
    summary="获取环境信息（支持条件查询）",
)
