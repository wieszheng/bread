# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/8 17:12
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.crud.auth.login import LoginCRUD
from app.schemas.login import UserLogin

router = APIRouter()


@router.post("/login", summary="用户登录")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    access_token = await LoginCRUD.create_access_token({"user_id": '1111'})
    request_from_swagger = request.headers.get('referer').endswith('docs') if request.headers.get('referer') else False
    request_from_redoc = request.headers.get('referer').endswith('redoc') if request.headers.get('referer') else False
    if request_from_swagger or request_from_redoc:
        return {'access_token': access_token, 'token_type': 'Bearer'}
    return {"msg": "登录成功", "token": access_token}
