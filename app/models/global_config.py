# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 14:37
@Author   : wiesZheng
@Software : PyCharm
"""
from sqlalchemy import BOOLEAN, INT, TEXT, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class GlobalConfig(BaseModel):
    """
    全局变量表
    """

    __tablename__ = "bread_global_config"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID"
    )
    env: Mapped[int] = mapped_column(INT, comment="环境名称")
    key: Mapped[str] = mapped_column(String(16), comment="名称键值")
    value: Mapped[str] = mapped_column(TEXT, comment="值")
    key_type: Mapped[int] = mapped_column(
        INT, default=0, comment="0: string 1: json 2: yaml"
    )
    enable: Mapped[bool] = mapped_column(BOOLEAN, default=True, comment="是否启用")
