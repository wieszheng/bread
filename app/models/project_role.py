#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/25 23:32
@Author   : wiesZheng
@Software : PyCharm
"""
from sqlalchemy import BOOLEAN, INT, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class ProjectRole(BaseModel):
    """
    项目角色表
    """

    __tablename__ = "bread_project_role"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID"
    )
    user_id: Mapped[int] = mapped_column(INT, index=True, comment="用户")
    project_id: Mapped[int] = mapped_column(INT, index=True, comment="项目")
    project_role: Mapped[int] = mapped_column(INT, index=True, comment="角色")
