# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/8 17:12
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter

from app.schemas.login import Token
from app.service.login_s import LoginService

router = APIRouter()

router.add_api_route(
    "/login",
    endpoint=LoginService.login,
    response_model=Token,
    methods=["post"],
    summary="用户登录"
)
