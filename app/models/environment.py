# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 14:37
@Author   : wiesZheng
@Software : PyCharm
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class Environment(BaseModel):
    """
    环境表
    """

    __tablename__ = "bread_environment"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID"
    )
    name: Mapped[str] = mapped_column(String(16), comment="环境名称")
    remarks: Mapped[str] = mapped_column(String(128), comment="备注信息")
