# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 11:50
@Author   : wiesZheng
@Software : PyCharm
"""
import traceback

from fastapi import FastAPI
from fastapi.requests import Request

from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import ValidationError

from app.commons.response.response_code import CustomResponseCode
from app.commons.response.response_schema import (
    InternalErrorException,
    ParameterException,
    CustomError,
    InvalidTokenException,
    ApiResponse,
    ForbiddenException,
)
from app.commons.schema import CUSTOM_VALIDATION_ERROR_MESSAGES

from app.exceptions.errors import TokenError, CustomException, AuthorizationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def register_exceptions_handler(app: FastAPI):
    """
    全局异常处理
    """

    @app.exception_handler(AuthorizationError)
    async def authorization_exception_handler(
        request: Request, exc: AuthorizationError
    ):
        logger.error(
            f"权限操作异常\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Message:{str(exc)}\n"
        )
        logger.error(traceback.format_exc())
        return ForbiddenException(message=str(exc))

    @app.exception_handler(TokenError)
    async def token_exception_handler(request: Request, exc: TokenError):
        logger.error(
            f"令牌操作异常\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Message:{str(exc)}\n"
        )
        logger.error(traceback.format_exc())
        return InvalidTokenException(message=str(exc))

    # 处理其他http请求异常
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """请求参数验证异常"""
        logger.warning(
            f"请求参数验证异常:\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Message:{exc.errors()}\n"
        )
        logger.error(traceback.format_exc())
        message = ".".join(
            [
                f'{".".join(map(lambda x: str(x), error.get("loc")))}:'
                f'{CUSTOM_VALIDATION_ERROR_MESSAGES.get(error.get("type")), error.get("msg")};'
                for error in exc.errors()
            ]
        )

        return ParameterException(
            message="请求参数校验错误,请检查提交的参数信息",
            result={"detail": message, "body": exc.body},
        )

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(
        request: Request, exc: ValidationError
    ):
        """内部参数验证异常"""
        logger.error(
            f"内部参数验证异常\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Message:{exc.errors()}\n"
        )
        message = ".".join(
            [
                f'{".".join(map(lambda x: str(x), error.get("loc")))}:'
                f'{CUSTOM_VALIDATION_ERROR_MESSAGES.get(error.get("type")), error.get("msg")};'
                for error in exc.errors()
            ]
        )
        logger.error(traceback.format_exc())

        return ParameterException(
            message="内部参数校验错误,请检查提交的参数信息", result={"detail": message}
        )

    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        """全局业务异常处理"""
        logger.warning(
            f"业务处理异常\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Code:{exc.err_code}\n"
            f"Message:{exc.err_code_des}\n"
        )

        return CustomError(
            code=exc.err_code,
            message=exc.err_code_des,
        )

    # 处理其他异常
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        """全局系统异常处理器"""
        if isinstance(exc, ConnectionError):
            message = f"网络异常: {exc}"
        else:
            message = f"未知异常: {exc}"

        logger.error(
            f"全局系统异常\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Message:{message}\n"
        )
        logger.error(traceback.format_exc())
        return InternalErrorException(result={"detail": str(exc)})

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handlers(request: Request, exc: StarletteHTTPException):
        logger.warning(
            f"Http请求异常\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Code:{exc.status_code}\n"
            f"Message:{exc.detail}\n"
        )

        exc_msg = CustomResponseCode.use_code_get_enum_msg(exc.status_code)
        return ApiResponse(
            http_status_code=exc.status_code,
            code=exc.status_code,
            message=exc_msg,
            success=False,
        )
