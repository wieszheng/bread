# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 15:04
@Author   : wiesZheng
@Software : PyCharm
"""

from fastapi import APIRouter

from app.core.security.Jwt import DependsJwtAuth
from app.service.config.global_config import GlobalConfigService

router = APIRouter(
    prefix="/config/global_config", tags=["全局变量"], dependencies=[DependsJwtAuth]
)

router.add_api_route(
    "",
    endpoint=GlobalConfigService.create_global_config,
    methods=["post"],
    summary="新增全局变量",
)

router.add_api_route(
    "",
    endpoint=GlobalConfigService.get_global_config,
    methods=["get"],
    summary="查询全局信息",
)

router.add_api_route(
    "",
    endpoint=GlobalConfigService.delete_global_config,
    methods=["delete"],
    summary="删除全局变量",
)

router.add_api_route(
    "",
    endpoint=GlobalConfigService.update_global_config,
    methods=["put"],
    summary="修改全局变量",
)

router.add_api_route(
    "/list",
    endpoint=GlobalConfigService.get_global_configs,
    methods=["get"],
    summary="获取全局变量（支持条件查询）",
)
