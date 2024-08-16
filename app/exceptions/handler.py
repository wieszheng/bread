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
from app.commons.response.response_schema import (MethodNotAllowedException, LimiterResException,
                                                  InternalErrorException, NotfoundException,
                                                  BadRequestException, OtherException, ParameterException,
                                                  BusinessError,
                                                  InvalidTokenException, ForbiddenException, ApiResponse)
from app.commons.schema import CUSTOM_VALIDATION_ERROR_MESSAGES

from app.exceptions.exception import BusinessException, AuthException, PermissionException, DBException
from starlette.exceptions import HTTPException as StarletteHTTPException


def register_exceptions_handler(app: FastAPI):
    """
    全局异常处理
    """

    # 自定义token检验异常
    @app.exception_handler(AuthException)
    async def auth_exception_handler(request: Request, exc: AuthException):
        """ 认证异常处理 """

        return InvalidTokenException()

    # 自定义权限检验异常
    @app.exception_handler(PermissionException)
    async def permission_exception_handler(request: Request, exc: PermissionException):
        return ForbiddenException()

    # 自定义数据库操作异常
    @app.exception_handler(DBException)
    async def db_exception_handler(request: Request, exc: DBException):
        return BusinessError(result={"err_code_des": exc.message})

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

        exc_msg = CustomResponseCode.use_code_get_enum_msg(exc.status_code)
        return ApiResponse(
            http_status_code=exc.status_code,
            result={},
            message=exc_msg,
            api_code=exc.status_code,
            success=False,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """ 请求参数验证异常 """
        logger.warning(
            f"Http请求异常: value_exception_handler\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Message:{exc.errors()}\n"
        )
        logger.error(traceback.format_exc())
        message = '.'.join([f'{".".join(map(lambda x: str(x), error.get("loc")))}:'
                            f'{CUSTOM_VALIDATION_ERROR_MESSAGES.get(error.get("type")), error.get("msg")};'
                            for error in exc.errors()])

        return ParameterException(
            message="请求参数校验错误,请检查提交的参数信息",
            result={"detail": message, "body": exc.body}
        )

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(request: Request, exc: ValidationError):
        """ 内部参数验证异常 """
        logger.error(
            f"内部参数验证异常\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Message:{exc.errors()}\n"
        )
        message = '.'.join([f'{".".join(map(lambda x: str(x), error.get("loc")))}:'
                            f'{CUSTOM_VALIDATION_ERROR_MESSAGES.get(error.get("type")), error.get("msg")};'
                            for error in exc.errors()])
        logger.error(traceback.format_exc())

        return ParameterException(
            message="内部参数校验错误,请检查提交的参数信息",
            result={"detail": message}
        )

    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        """ 全局业务异常处理 """
        logger.warning(
            f"业务处理异常\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Code:{exc.err_code}\n"
            f"Message:{exc.err_code_des}\n"
        )

        return BusinessError(api_code=exc.err_code, result={"err_code_des": exc.err_code_des})

    # 处理其他异常
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        """ 全局系统异常处理器 """
        if isinstance(exc, ConnectionError):
            message = f'网络异常 --> {traceback.format_exc()}'
        else:
            message = f'系统异常 --> {traceback.format_exc()}'

        logger.error(
            f"全局系统异常\n"
            f"Method:{request.method}\n"
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"Message:{message}\n"
        )

        return InternalErrorException(result={"detail": str(exc)})
