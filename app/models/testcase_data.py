#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/12 0:17
@Author   : wiesZheng
@Software : PyCharm
"""

from sqlalchemy import INT, TEXT, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class TestCaseData(BaseModel):
    """
    用例数据表
    """

    __tablename__ = 'bread_testcase_data'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment='主键ID'
    )
    env: Mapped[int] = mapped_column(INT, nullable=False, comment='环境ID')
    case_id: Mapped[int] = mapped_column(INT, nullable=False, comment='用例ID')
    name: Mapped[str] = mapped_column(String(32), nullable=False, comment='名称')
    json_data: Mapped[str] = mapped_column(TEXT, nullable=False, comment='json数据')
