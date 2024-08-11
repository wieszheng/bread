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

from app.commons import R
from app.commons.resq import (MethodNotAllowedException, LimiterResException, InternalErrorException, NotfoundException,
                              BadRequestException, OtherException, ParameterException, BusinessError,
                              InvalidTokenException, ForbiddenException)

from app.exceptions.exception import BusinessException, AuthException, PermissionException
from starlette.exceptions import HTTPException as StarletteHTTPException


def register_exceptions_handler(app: FastAPI):
    """
    全局异常处理
    """

    # 自定义token检验异常
    @app.exception_handler(AuthException)
    async def auth_exception_handler(request: Request, exc: AuthException):
        """ 认证异常处理 """
        logger.info('认证失败')
        return InvalidTokenException()

    # 自定义权限检验异常
    @app.exception_handler(PermissionException)
    async def permission_exception_handler(request: Request, exc: PermissionException):
        return ForbiddenException()

    # 处理其他http请求异常
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
        match exc.status_code:
            case 405:
                return MethodNotAllowedException()
            case 404:
                return NotfoundException()
            case 429:
                return LimiterResException()
            case 500:
                return InternalErrorException()
            case 400:
                return BadRequestException(message=exc.detail)
            case _:
                return OtherException(message=str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """ 全局捕捉参数验证异常 """
        message = '.'.join([f'{".".join(map(lambda x: str(x), error.get("loc")))}:{error.get("msg")};'
                            for error in exc.errors()])

        logger.warning(message)
        return ParameterException(result={"detail": message, "body": exc.body})

    @app.exception_handler(ValueError)
    async def value_exception_handler(request: Request, exc: ValueError):
        """
        捕获值异常
        """
        logger.warning(
            f"Http请求异常: value_exception_handler\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Message:{exc.__str__()}\n"
        )
        # logger.exception(str(exc))
        ParameterException(result={"detail": str(exc.__str__())})

    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        """ 全局业务异常处理 """
        logger.info(
            f"Http请求异常\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Code:{exc.err_code}\n"
            f"Message:{exc.err_code_des}\n"
        )

        return BusinessError(api_code=exc.err_code, message=exc.err_code_des)

    # 处理其他异常
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        """ 全局系统异常处理器 """
        # logger.exception(exc)

        if isinstance(exc, ConnectionError):
            message = f'网络异常, {traceback.format_exc()}'
        else:
            message = f'系统异常, {traceback.format_exc()}'

        logger.error(message)
        return InternalErrorException(result={"detail": message})
