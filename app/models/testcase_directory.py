# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/11 12:11
@Author   : wiesZheng
@Software : PyCharm
"""

from sqlalchemy import INT, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class TestcaseDirectory(BaseModel):
    """
    用例目录表
    """

    __tablename__ = "bread_testcase_directory"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID"
    )
    project_id: Mapped[int] = mapped_column(INT, index=True, comment="项目id")
    name: Mapped[str] = mapped_column(String(16), nullable=False, comment="目录名称")
    parent: Mapped[int | None] = mapped_column(INT, comment="上传目录")
