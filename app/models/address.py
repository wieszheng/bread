# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 14:37
@Author   : wiesZheng
@Software : PyCharm
"""

from sqlalchemy import INT, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class Address(BaseModel):
    """
    地址表
    """

    __tablename__ = "bread_address"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID"
    )
    env: Mapped[int] = mapped_column(INT, comment="对应环境名称")
    name: Mapped[str] = mapped_column(String(16), comment="网关名称")
    gateway: Mapped[str] = mapped_column(String(128), comment="网关地址")
