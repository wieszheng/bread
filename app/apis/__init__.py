# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:54
@Author   : wiesZheng
@Software : PyCharm
"""

from fastapi import APIRouter, FastAPI
from loguru import logger

from ..apis.v1 import router as v1_router

router = APIRouter(prefix='/api')
router.include_router(v1_router)


async def register_routers(app: FastAPI):
    logger.info('注册路由')
    app.include_router(router)
