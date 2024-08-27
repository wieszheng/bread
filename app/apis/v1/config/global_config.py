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

router = APIRouter(prefix="/config/global_config", tags=["全局变量"])

router.add_api_route(
    "",
    endpoint=GlobalConfigService.create_global_config,
    dependencies=[DependsJwtAuth],
    methods=["post"],
    summary="新增全局变量",
)
