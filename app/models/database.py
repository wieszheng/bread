#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/9 23:42
@Author   : wiesZheng
@Software : PyCharm
"""

from sqlalchemy import INT, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel
from app.models.environment import Environment


class DataBase(BaseModel):
    """
    数据库信息表
    """

    __tablename__ = 'bread_database_info'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment='主键ID'
    )
    env: Mapped[int] = mapped_column(INT, comment='对应环境名称')
    name: Mapped[str] = mapped_column(String(24), nullable=False, comment='数据库名称')
    host: Mapped[str] = mapped_column(String(64), nullable=False, comment='数据库地址')
    port: Mapped[int] = mapped_column(INT, nullable=False, comment='端口')
    username: Mapped[str] = mapped_column(String(36), nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    database: Mapped[str] = mapped_column(String(36), nullable=False)
    sql_type = mapped_column(
        INT, nullable=False, comment='0: mysql 1: postgresql 2: mongo'
    )
    env_info: Environment
