# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/14 10:57
@Author   : wiesZheng
@Software : PyCharm
"""
import jwt
import pytz
from typing import Dict, Any, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidSignatureError, DecodeError, ExpiredSignatureError

from app.exceptions.exception import AuthException
from config import JwtConfig

# 设置时区
ChinaTimeZone = pytz.timezone("Asia/Shanghai")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/login')


async def create_access_token(payload: Dict[Any, Union[str, Any]]) -> str:
    """
    根据登录信息创建当前用户token

    :param payload: 用户信息
    :return: token
    """
    current_time = datetime.now(ChinaTimeZone)
    new_data = dict({
        "jti": current_time.strftime("%Y%m%d%H%M%f"),
        "iss": JwtConfig.JWT_ISS,
        "iat": current_time,
        "exp": current_time + timedelta(minutes=JwtConfig.JWT_EXPIRE_MINUTES)},
        **payload)
    # 生成并返回jwt
    return jwt.encode(new_data,
                      key=JwtConfig.JWT_SECRET_KEY,
                      algorithm=JwtConfig.JWT_ALGORITHM)


async def decode_jwt_token(token: str) -> dict:
    if not token:
        raise AuthException(message="用户信息身份认证失败, 请检查")
    try:
        return jwt.decode(token, JwtConfig.JWT_SECRET_KEY, algorithms=[JwtConfig.JWT_ALGORITHM])

    except (InvalidSignatureError, DecodeError):
        raise AuthException(message="无效认证，请重新登录")

    except ExpiredSignatureError:
        raise AuthException()
