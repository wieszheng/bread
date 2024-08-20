#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/17 13:01
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import Any

from fastapi import Request, Response
from fastapi.security.utils import get_authorization_scheme_param
from loguru import logger

from starlette.requests import HTTPConnection
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)

from app.commons.response.response_schema import ApiResponse
from app.core.security import Jwt
from app.exceptions.errors import TokenError
from app.schemas.auth.user import CurrentUserIns


class _AuthenticationError(AuthenticationError):
    """重写内部认证错误类"""

    def __init__(
        self,
        *,
        code: int = None,
        msg: str = None,
        headers: dict[str, Any] | None = None
    ):
        self.code = code
        self.msg = msg
        self.headers = headers


class JwtAuthMiddleware(AuthenticationBackend):
    """JWT 认证中间件"""

    @staticmethod
    def auth_exception_handler(
        conn: HTTPConnection, exc: _AuthenticationError
    ) -> Response:
        """覆盖内部认证错误处理"""

        return ApiResponse(
            http_status_code=exc.code, api_code=exc.code, message=exc.msg
        )

    async def authenticate(
        self, request: Request
    ) -> tuple[AuthCredentials, CurrentUserIns] | None:
        token = request.headers.get("Authorization")
        if not token:
            return

        scheme, token = get_authorization_scheme_param(token)
        if scheme.lower() != "bearer":
            return
        sub = await Jwt.decode_jwt_token(token)
        current_user = await Jwt.get_current_user(sub)
        user = CurrentUserIns.model_validate(current_user)

        return AuthCredentials(["authenticated"]), user
