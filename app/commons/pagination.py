# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/19 16:42
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import Generic, TypeVar, Sequence

from pydantic import BaseModel

T = TypeVar("T")
DataT = TypeVar("DataT")


class _Page(Generic[T]):
    items: Sequence[T]  # 数据
    total: int  # 总数据数
    page: int  # 第n页
    size: int  # 每页数量
    total_pages: int  # 总页数


class _PageData(BaseModel, Generic[DataT]):
    page_data: list[DataT] | None = None
