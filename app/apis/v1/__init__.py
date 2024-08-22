# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:55
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter, FastAPI
from loguru import logger

from app.apis.v1.auth import user
from app.apis.v1.project import project

v1 = APIRouter(prefix="/v1")

RegisterRouterList = [user, project]

for item in RegisterRouterList:
    v1.include_router(item.router)


async def register_routers(app: FastAPI):
    logger.info("注册路由")
    app.include_router(v1, prefix="/api")
