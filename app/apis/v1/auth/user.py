# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:55
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["用户接口"])


@router.post("/login", summary="用户登录")
async def login():
    return {"code": 0, "msg": "登录成功"}
