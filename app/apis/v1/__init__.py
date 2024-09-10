# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:55
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter

from app.apis.v1.auth import user
from app.apis.v1.config import address, environment, global_config
from app.apis.v1.project import project
from app.apis.v1.testcase import testcase

router = APIRouter(prefix="/v1")

RegisterRouterList = [user, project, address, environment, global_config, testcase]

for item in RegisterRouterList:
    router.include_router(item.router)
