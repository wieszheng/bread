# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 10:59
@Author   : wiesZheng
@Software : PyCharm
"""
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    MappedAsDataclass,
)
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import settings

# 定义数据库URL
async_database_url = URL.create(
    settings.MYSQL_PROTOCOL,
    settings.MYSQL_USERNAME,
    settings.MYSQL_PASSWORD,
    settings.MYSQL_HOST,
    settings.MYSQL_PORT,
    settings.MYSQL_DATABASE,
    {"charset": "utf8mb4"},
)
# 创建异步引擎
async_engine = create_async_engine(
    async_database_url,
    echo=settings.MYSQL_ECHO,
    pool_size=settings.MYSQL_POOL_SIZE,
    pool_recycle=settings.MYSQL_POOL_RECYCLE,
    pool_timeout=settings.MYSQL_POOL_TIMEOUT,
)

# 初始化Session工厂
async_session_maker = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, autocommit=False, expire_on_commit=False
)


class Base(AsyncAttrs, DeclarativeBase):
    """SQLAlchemy Base ORM Model"""

    __abstract__ = True

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self, *ignore: str, alias_dict: dict = None, exclude_none=True) -> dict:
        """
        数据库模型转成字典
        Args:
            ignore (list): 屏蔽字段，建议使用BaseModel
            alias_dict: 字段别名字典
                eg: {"id": "user_id"}, 把id名称替换成 user_id
            exclude_none: 默认排查None值
        Returns: dict
        """

        alias_dict = alias_dict or {}
        if exclude_none:
            return {
                alias_dict.get(c.name, c.name): (
                    getattr(self, c.name).strftime("%Y-%m-%d %H:%M:%S")
                    if isinstance(getattr(self, c.name), datetime)
                    else getattr(self, c.name)
                )
                for c in self.__table__.columns
                if getattr(self, c.name) is not None and c.name not in ignore
            }
        else:
            return {
                alias_dict.get(c.name, c.name): (
                    getattr(self, c.name, None).strftime("%Y-%m-%d %H:%M:%S")
                    if isinstance(getattr(self, c.name, None), datetime)
                    else getattr(self, c.name, None)
                )
                for c in self.__table__.columns
            }


class TimestampMixin(AsyncAttrs, DeclarativeBase):
    """时间戳相关列"""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now, comment="创建时间"
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )


class SoftDeleteMixin(AsyncAttrs, DeclarativeBase):
    deleted_at: Mapped[datetime | None] = mapped_column(
        default=None, comment="删除时间"
    )
    is_deleted: Mapped[bool] = mapped_column(
        default=False, index=True, comment="是否逻辑删除"
    )


class OperatorMixin(AsyncAttrs, DeclarativeBase):
    """操作人相关列"""

    __abstract__ = True

    created_by: Mapped[int | None] = mapped_column(default=None, comment="创建人")

    updated_by: Mapped[int | None] = mapped_column(default=None, comment="更新人")


class BaseModel(Base, TimestampMixin, SoftDeleteMixin, OperatorMixin):
    __abstract__ = True
