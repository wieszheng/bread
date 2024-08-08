# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:55
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter
from app.apis.v1.auth import user, login

v1 = APIRouter(prefix="/v1")

RegisterRouterList = [
    user,
    login
]

for item in RegisterRouterList:
    v1.include_router(item.router)
