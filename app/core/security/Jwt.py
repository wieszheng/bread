# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/16 10:40
@Author   : wiesZheng
@Software : PyCharm
"""

from datetime import datetime, timedelta

import jwt
import pytz
from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError

from app.exceptions.errors import AuthorizationException, TokenError
from app.schemas.auth.user import CurrentUserInfo
from config import settings

# 设置时区
ChinaTimeZone = pytz.timezone("Asia/Shanghai")
DependsJwtAuth = Depends(HTTPBearer())


async def create_access_token(
    sub: str, expires_delta: timedelta | None = None, **kwargs
) -> str:
    """
    根据登录信息创建当前用户token

    :param sub: 用户信息
    :param expires_delta:
    :return: token
    """
    current_time = datetime.now(ChinaTimeZone)
    if expires_delta:
        expire = current_time + expires_delta
    else:
        expire = current_time + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    to_encode = {
        "jti": current_time.strftime("%Y%m%d%H%M%f"),
        "iss": settings.JWT_ISS,
        "iat": current_time,
        "exp": expire,
        "sub": sub,
        **kwargs,
    }

    # 生成并返回jwt
    return jwt.encode(
        to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


async def decode_jwt_token(token: str) -> int:
    """
    Decode token

    :param token:
    :return:
    """
    # if not token or len(token.strip()) < 5:
    #     raise ValueError("Token不能为空或长度过短")
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        if not user_id:
            raise AuthorizationException(message="签名验证失败，请检查Token是否被篡改")
    except InvalidSignatureError:
        raise AuthorizationException(message="签名验证失败，请检查Token是否被篡改")
    except ExpiredSignatureError:
        raise AuthorizationException(message="很久没操作，令牌Token过期")
    except DecodeError:
        raise AuthorizationException(message="解码失败，请检查Token格式")
    return user_id


async def get_current_user(pk: int):
    """
    Get the current user through token

    :param pk:
    :return:
    """
    from app.crud.auth.user import UserCRUD

    user = await UserCRUD.get(id=pk)
    if not user:
        raise TokenError(message="非法Token，请检查提交信息")
    if not user["is_valid"]:
        raise AuthorizationException(message="用户已被锁定，请联系系统管理员")

    return user


async def get_current_user_new(request: Request):
    """
    Get the current user through token

    :param request:
    :param token:
    :return:
    """
    from app.crud.auth.user import UserCRUD

    token = request.headers.get("Authorization")
    if not token:
        return

    scheme, token = get_authorization_scheme_param(token)
    if scheme.lower() != "bearer":
        return

    sub = await decode_jwt_token(token)
    user = await UserCRUD.get(id=sub)
    if not user["is_valid"]:
        raise AuthorizationException(message="用户已被锁定，请联系系统管理员")

    return CurrentUserInfo(**user)
