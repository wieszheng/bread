#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/12 0:13
@Author   : wiesZheng
@Software : PyCharm
"""
from sqlalchemy import String, INT, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class TestCaseAsserts(BaseModel):
    """
    用例断言表
    """
    __tablename__ = "bread_testcase_asserts"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID"
    )
    name: Mapped[str] = mapped_column(String(32), nullable=False, comment="名称")
    case_id: Mapped[int] = mapped_column(INT, index=True, comment="用例ID")
    assert_type: Mapped[str] = mapped_column(String(16), comment="断言类型 equal: 等于 not_equal: 不等于 in: 属于")
    expected: Mapped[str] = mapped_column(TEXT, nullable=False, comment="预期结果")
    actually: Mapped[str] = mapped_column(TEXT, nullable=False, comment="实际结果")
