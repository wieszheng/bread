# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/16 10:40
@Author   : wiesZheng
@Software : PyCharm
"""
import jwt
import pytz

from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import HTTPBearer
from jwt import InvalidSignatureError, DecodeError, ExpiredSignatureError

from app.exceptions.errors import TokenError, AuthorizationError
from config import JwtConfig

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
        expire = current_time + timedelta(minutes=JwtConfig.JWT_EXPIRE_MINUTES)

    to_encode = {
        "jti": current_time.strftime("%Y%m%d%H%M%f"),
        "iss": JwtConfig.JWT_ISS,
        "iat": current_time,
        "exp": expire,
        "sub": sub,
        **kwargs,
    }

    # 生成并返回jwt
    return jwt.encode(
        to_encode, key=JwtConfig.JWT_SECRET_KEY, algorithm=JwtConfig.JWT_ALGORITHM
    )


async def decode_jwt_token(token: str) -> int:
    """
    Decode token

    :param token:
    :return:
    """
    try:
        payload = jwt.decode(
            token, JwtConfig.JWT_SECRET_KEY, algorithms=[JwtConfig.JWT_ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        if not user_id:
            raise TokenError("非法操作，令牌无效")
    except (InvalidSignatureError, DecodeError):
        raise TokenError("非法操作，令牌无效")
    except ExpiredSignatureError:
        raise TokenError("很久没操作，令牌过期")
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
        raise TokenError("很久没操作，令牌失效")
    if user["is_valid"]:
        raise AuthorizationError("用户已被锁定，请联系系统管理员")

    return user
