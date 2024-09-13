#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/13 23:42
@Author   : wiesZheng
@Software : PyCharm
"""

from sqlalchemy import BOOLEAN, String, TEXT, INT
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class Constructor(BaseModel):
    """
    前后置数据
    """

    __tablename__ = 'bread_constructor'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment='主键ID'
    )
    type: Mapped[int] = mapped_column(
        INT, default=0, comment='0: testcase 1: sql 2: redis 3: py脚本 4: 其它'
    )
    name: Mapped[str] = mapped_column(String(64), comment='数据初始化描述')
    enable: Mapped[bool] = mapped_column(BOOLEAN, default=True, nullable=False)
    constructor_json: Mapped[str] = mapped_column(TEXT, nullable=False)
    value: Mapped[str] = mapped_column(String(16), comment='返回值')
    case_id: Mapped[int] = mapped_column(INT, nullable=False, comment='所属用例id')
    public: Mapped[bool] = mapped_column(BOOLEAN, default=False, comment='是否共享')
    index: Mapped[int] = mapped_column(INT, default=0, comment='前置条件顺序')
    # 2021-12-18 是否是后置条件
    suffix: Mapped[bool] = mapped_column(
        BOOLEAN, default=False, comment='是否是后置条件，默认为否'
    )
