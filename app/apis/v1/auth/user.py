# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:55
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/login')

router = APIRouter(prefix="/system/user", tags=["用户接口"])


@router.post("/me", summary="用户")
async def login(token: str = Depends(oauth2_scheme)):

    return {"code": 0, "msg": token}
