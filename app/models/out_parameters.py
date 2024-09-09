#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 0:01
@Author   : wiesZheng
@Software : PyCharm
"""
from sqlalchemy import INT, SMALLINT, TEXT, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class TestCaseOutParameters(BaseModel):
    """
    用例参数据表
    """

    __tablename__ = "bread_out_parameters"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID"
    )
    case_id = mapped_column(INT, nullable=False, comment="用例id")
    name = mapped_column(String(24), nullable=False, comment="参数名")
    source = mapped_column(
        INT,
        nullable=False,
        default=0,
        comment="来源类型0: Body(TEXT) 1: Body(JSON) 2: Header 3: Cookie 4: HTTP状态码",
    )
    expression = mapped_column(String(128), comment="表达式")
    # 获取结果索引, 可以是random，也可以是all，还可以是数字
    match_index = mapped_column(String(16), comment="主键ID")
