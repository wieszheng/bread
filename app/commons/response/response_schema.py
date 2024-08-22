# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 11:11
@Author   : wiesZheng
@Software : PyCharm
"""
import datetime
import decimal
import inspect
import json
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.declarative import DeclarativeMeta

from app.commons.response.response_code import CustomResponseCode


class ResponseModel(BaseModel):
    """
    统一返回模型
    E.g. ::
        @router.get('/test', response_model=ResponseModel)
        def test():
            return ResponseModel(data={'test': 'test'})
    """

    success: bool
    code: int = CustomResponseCode.HTTP_200.code
    message: str = CustomResponseCode.HTTP_200.msg
    result: Optional[Dict[str, Any]] = None


class ListPageRequestModel(BaseModel):
    """分页请求模型"""

    page: int = Field(default=1, ge=1, description="分页偏移量")
    page_size: int = Field(default=10, gt=1, description="每页显示数量")
    query_params: Optional[dict] = Field(default={}, description="查询参数")
    orderings: Optional[List[str]] = Field(default=["id"], description="排序字段")


class ListResponseDataModel(BaseModel):
    """分页列表响应data模型"""

    total: int = Field(default=0, description="数据总数量")
    data_list: list = Field(default=[], description="数据列表")
    has_more: bool = Field(default=False, description="是否有下一页")
    next_offset: int = Field(default=0, description="offset下次起步")


class ListResponseModel(ResponseModel):
    """分页列表响应统一返回"""

    result: ListResponseDataModel


class ResponseBase:
    """
    统一返回方法

    .. tip::

        此类中的方法将返回 ResponseModel 模型，作为一种编码风格而存在；

    E.g. ::

        @router.get('/test')
        def test() -> ResponseModel:
            return await response_base.success(data={'test': 'test'})
    """

    @staticmethod
    async def __response(
        *,
        res: CustomResponseCode = None,
        result: Optional[Dict[str, Any]] = None,
        success: bool = False,
    ) -> ResponseModel:
        """
        请求成功返回通用方法

        :param res: 返回信息
        :param result: 返回数据
        :return:
        """
        return ResponseModel(success=success, code=res.code, msg=res.msg, result=result)

    @classmethod
    async def success(
        cls,
        *,
        res: CustomResponseCode = CustomResponseCode.HTTP_200,
        result: Optional[Dict[str, Any]] = None,
    ) -> ResponseModel:
        return await cls.__response(res=res, result=result, success=True)

    @classmethod
    async def fail(
        cls,
        *,
        res: CustomResponseCode = CustomResponseCode.HTTP_400,
        result: Optional[Dict[str, Any]] = None,
    ) -> ResponseModel:
        return await cls.__response(res=res, result=result)


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # 如果对象具有keys和__getitem__属性，则返回对象的字典表示
        if hasattr(obj, "keys") and hasattr(obj, "__getitem__"):
            return dict(obj)
        # 如果对象是datetime.datetime类型，则将其转换为字符串格式
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        # 如果对象是datetime.date类型，则将其转换为字符串格式
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        # 如果对象是datetime.time类型，则将其转换为ISO格式字符串
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        # 如果对象是decimal.Decimal类型，则将其转换为浮点数
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        # 如果对象是bytes类型，则将其转换为UTF-8编码的字符串
        elif isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        # 如果对象的类是DeclarativeMeta类型，则将其序列化为JSON
        elif isinstance(obj.__class__, DeclarativeMeta):
            # 如果是查询返回所有的那种models类型的，需要处理些
            # 将SqlAlchemy结果序列化为JSON--查询全部的时候的处理返回
            return self.default(
                {i.name: getattr(obj, i.name) for i in obj.__table__.columns}
            )
        # 如果对象是字典类型，则递归处理其中的值
        elif isinstance(obj, dict):
            for k in obj:
                try:
                    if isinstance(
                        obj[k], (datetime.datetime, datetime.date, DeclarativeMeta)
                    ):
                        obj[k] = self.default(obj[k])
                    else:
                        obj[k] = obj[k]
                except TypeError:
                    obj[k] = None
            return obj

        # 默认情况下，使用JSONEncoder的默认处理方式
        return json.JSONEncoder.default(self, obj)


class ApiResponse(JSONResponse):
    # 定义返回响应码--如果不指定的话则默认都是返回200
    http_status_code = 200
    # 默认成功
    code = 200
    success = True
    message = "success"
    result: Optional[Dict[str, Any]] = None  # 结果可以是{} 或 []

    def __init__(
        self,
        success=None,
        http_status_code=None,
        code=None,
        result=None,
        message=None,
        **kwargs,
    ):
        self.message = message or self.message
        self.code = code or self.code
        self.success = success or self.success
        self.http_status_code = http_status_code or self.http_status_code
        self.result = result or self.result

        # 返回内容体
        content = dict(
            message=self.message,
            code=self.code,
            success=self.success,
            result=self.result,
        )
        content.update(kwargs)
        super(ApiResponse, self).__init__(
            status_code=self.http_status_code,
            content=content,
            media_type="application/json;charset=utf-8",
        )

    # 这个render会自动调用，如果这里需要特殊的处理的话，可以重写这个地方
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=CJsonEncoder,
        ).encode("utf-8")


class Success(ApiResponse):
    http_status_code = 200
    code = 200
    result = None  # 结果可以是{} 或 []
    message = "请求成功"
    success = True


class Fail(ApiResponse):
    http_status_code = 200
    code = -1
    result = None  # 结果可以是{} 或 []
    message = "操作失败"
    success = False


class BadRequestException(ApiResponse):
    http_status_code = 400
    code = 10031
    result = None  # 结果可以是{} 或 []
    message = "错误的请求"
    success = False


class ParameterException(ApiResponse):
    http_status_code = 400
    result = {}
    message = "参数校验错误,请检查提交的参数信息"
    code = 10031
    success = False


class CustomError(ApiResponse):
    http_status_code = 200
    code = 0000
    result = None  # 结果可以是{} 或 []
    message = "业务错误逻辑处理"
    success = False


class InternalErrorException(ApiResponse):
    http_status_code = 500
    result = {}
    message = "程序员哥哥睡眠不足，系统崩溃了！"
    code = 5000
    success = False


class LimiterResException(ApiResponse):
    http_status_code = 429
    code = 429
    result = None  # 结果可以是{} 或 []
    message = "访问的速度过快"
    success = False


class UnauthorizedException(ApiResponse):
    http_status_code = 401
    result = {}
    message = "未经许可授权"
    code = 10032
    success = False


class ForbiddenException(ApiResponse):
    http_status_code = 403
    result = {}
    message = "失败！当前访问没有权限，或操作的数据没权限!"
    code = 10033
    success = False


class NotfoundException(ApiResponse):
    http_status_code = 404
    result = {}
    message = "访问地址不存在"
    code = 10034
    success = False


class MethodNotAllowedException(ApiResponse):
    http_status_code = 405
    result = {}
    message = "不允许使用此方法提交访问"
    code = 10034
    success = False


class OtherException(ApiResponse):
    http_status_code = 200
    result = {}
    message = "未知的其他HTTP PARAMETER异常"
    code = 10034
    success = False


class InvalidTokenException(ApiResponse):
    http_status_code = 401
    code = 401
    message = "很久没操作，令牌失效"
    success = False


class ExpiredTokenException(ApiResponse):
    http_status_code = 422
    message = "很久没操作，令牌过期"
    code = 10050
    success = False


class FileTooLargeException(ApiResponse):
    http_status_code = 413
    code = 413
    result = None  # 结果可以是{} 或 []
    message = "文件体积过大"


class FileTooManyException(ApiResponse):
    http_status_code = 413
    message = "文件数量过多"
    code = 10120
    result = None  # 结果可以是{} 或 []


class FileExtensionException(ApiResponse):
    http_status_code = 401
    message = "文件扩展名不符合规范"
    code = 10121
    result = None  # 结果可以是{} 或 []


RT = TypeVar("RT")


def unified_resp(func: Callable[..., RT]):
    @wraps(func)
    async def wrapper(*args, **kwargs) -> RT:
        if inspect.iscoroutinefunction(func):

            resp = await func(*args, **kwargs) or []
        else:
            resp = func(*args, **kwargs) or []
        return Success(result=resp)

    return wrapper
