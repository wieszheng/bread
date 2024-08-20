#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/20 23:29
@Author   : wiesZheng
@Software : PyCharm
"""
from sqlalchemy import String, INT, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class ProjectModel(BaseModel):
    """
    项目表
    """

    __tablename__ = "project"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID"
    )
    name: Mapped[str] = mapped_column(String(16), comment="项目名称")
    owner: Mapped[int] = mapped_column(INT, comment="项目所有者")
    app: Mapped[str] = mapped_column(String(32), comment="项目所属应用")
    private: Mapped[bool] = mapped_column(BOOLEAN, default=False, comment="是否私有")
    description: Mapped[str | None] = mapped_column(String(200), comment="项目描述")
    avatar: Mapped[str | None] = mapped_column(
        String(128), default=None, comment="项目头像"
    )
    dingtalk_url: Mapped[str | None] = mapped_column(
        String(128), default=None, comment="钉钉通知url"
    )
