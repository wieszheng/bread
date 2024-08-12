# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/12 12:48
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import Dict, Any, Union

import jwt
import pytz
from fastapi import Request, Depends
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import InvalidTokenError
from loguru import logger

from app.commons.resq import Success

from app.exceptions.exception import AuthException
from app.schemas.login import UserLoginIn
from config import JwtConfig

# 设置时区
ChinaTimeZone = pytz.timezone("Asia/Shanghai")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/login')


class LoginService:
    @classmethod
    async def create_access_token(cls, payload: Dict[Any, Union[str, Any]]):
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

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)):
        """
        根据token获取当前用户信息
        """
        try:
            if token.startswith('Bearer'):
                token = token.split(' ')[1]
            payload = jwt.decode(token, JwtConfig.JWT_SECRET_KEY, algorithms=[JwtConfig.JWT_ALGORITHM])
            print(payload)
            user_id: str = payload.get('user_id')
            if not user_id:
                logger.warning('用户token不合法')
                raise AuthException(message='用户token不合法')

        except InvalidTokenError:
            logger.warning('用户token已失效，请重新登录')
            raise AuthException(message='用户token已失效，请重新登录')
        # user_info = await UserCRUD.get_user_info(id=user_id)
        return "user_info"

    @classmethod
    async def login(cls, request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
        user = UserLoginIn(**dict(
            username=form_data.username,
            password=form_data.password
        ))

        access_token = await cls.create_access_token({"user_id": '1111'})
        request_from_swagger = request.headers.get('referer').endswith('docs') if request.headers.get(
            'referer') else False
        request_from_redoc = request.headers.get('referer').endswith('redoc') if request.headers.get(
            'referer') else False
        if request_from_swagger or request_from_redoc:
            return {'access_token': access_token, 'token_type': 'Bearer'}
        return Success(
            result={'access_token': access_token, 'token_type': 'Bearer'},
            message='登录成功'
        )
