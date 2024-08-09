# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 15:07
@Author   : wiesZheng
@Software : PyCharm
"""
from functools import wraps
from typing import Any, Optional, Callable, Union

from loguru import logger
from sqlalchemy import ColumnElement, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.util import AliasedClass

from app.commons.types import ModelType, CreateSchemaType
from app.models import async_session_maker


def with_session(method):
    """
    兼容事务
    Args:
        method: orm 的 crud
    Notes:
        方法中没有带事务连接则，则构造
    Returns:
    """

    @wraps(method)
    async def wrapper(db_manager, *args, **kwargs):
        try:
            session = kwargs.get("session") or None
            if session:
                return await method(db_manager, *args, **kwargs)
            else:
                async with async_session_maker() as session:
                    async with session.begin():
                        kwargs["session"] = session
                        return await method(db_manager, *args, **kwargs)
        except Exception as e:
            import traceback
            logger.exception(traceback.format_exc())
            logger.error(
                f"操作 {db_manager.orm_table.__name__} 失败\n"
                f"args：{[*args]}, kwargs：{kwargs}\n"
                f"方法：{method.__name__}\n"
                f"{e}\n"
            )

    return wrapper


class BaseCRUD:
    _SUPPORTED_FILTERS = {
        "gt": lambda column: column.__gt__,
        "lt": lambda column: column.__lt__,
        "gte": lambda column: column.__ge__,
        "lte": lambda column: column.__le__,
        "ne": lambda column: column.__ne__,
        "is": lambda column: column.is_,
        "is_not": lambda column: column.is_not,
        "like": lambda column: column.like,
        "notlike": lambda column: column.notlike,
        "ilike": lambda column: column.ilike,
        "notilike": lambda column: column.notilike,
        "startswith": lambda column: column.startswith,
        "endswith": lambda column: column.endswith,
        "contains": lambda column: column.contains,
        "match": lambda column: column.match,
        "between": lambda column: column.between,
        "in": lambda column: column.in_,
        "not_in": lambda column: column.not_in,
    }

    def __init__(
            self,
            model: type[ModelType],
            is_deleted_column: str = "is_deleted",
            deleted_at_column: str = "deleted_at",
            updated_at_column: str = "updated_at",
    ) -> None:
        self.model = model
        self.model_col_names = [col.key for col in model.__table__.columns]
        self.is_deleted_column = is_deleted_column
        self.deleted_at_column = deleted_at_column
        self.updated_at_column = updated_at_column
        # self._primary_keys = _get_primary_keys(self.model)

    def _get_sqlalchemy_filter(
            self,
            operator: str,
            value: Any,
    ) -> Optional[Callable[[str], Callable]]:
        if operator in {"in", "not_in", "between"}:
            if not isinstance(value, (tuple, list, set)):
                raise ValueError(f"<{operator}> filter must be tuple, list or set")
        return self._SUPPORTED_FILTERS.get(operator)

    def _parse_filters(
            self, model: Optional[Union[type[ModelType], AliasedClass]] = None, **kwargs
    ) -> list[ColumnElement]:
        model = model or self.model
        filters = []

        for key, value in kwargs.items():
            if "__" in key:
                field_name, op = key.rsplit("__", 1)
                column = getattr(model, field_name, None)
                if column is None:
                    raise ValueError(f"Invalid filter column: {field_name}")
                if op == "or":
                    or_filters = [
                        sqlalchemy_filter(column)(or_value)
                        for or_key, or_value in value.items()
                        if (
                               sqlalchemy_filter := self._get_sqlalchemy_filter(
                                   or_key, value
                               )
                           )
                           is not None
                    ]
                    filters.append(or_(*or_filters))
                else:
                    sqlalchemy_filter = self._get_sqlalchemy_filter(op, value)
                    if sqlalchemy_filter:
                        filters.append(sqlalchemy_filter(column)(value))
            else:
                column = getattr(model, key, None)
                if column is not None:
                    filters.append(column == value)

        return filters

    @with_session
    async def create(
            self, *, obj: CreateSchemaType, commit: bool = True, session: AsyncSession = None
    ) -> ModelType:

        object_dict = obj.model_dump()
        object_mt: ModelType = self.model(**object_dict)
        session.add(object_mt)
        if commit:
            await session.commit()
        return object_mt
