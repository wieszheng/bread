#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/9 23:50
@Author   : wiesZheng
@Software : PyCharm
"""

from datetime import datetime

from sqlalchemy import INT, SMALLINT, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class Report(BaseModel):
    """
    执行结果表
    """

    __tablename__ = 'bread_report'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment='主键ID'
    )
    env: Mapped[int] = mapped_column(INT, comment='对应环境名称')
    executor: Mapped[int] = mapped_column(INT, index=True, comment='对应环境名称')
    cost: Mapped[str] = mapped_column(String(8))
    plan_id: Mapped[int] = mapped_column(
        INT, index=True, nullable=True, comment='测试集合id，预留字段'
    )
    start_at: Mapped[datetime] = mapped_column(nullable=False, comment='开始时间')
    finished_at: Mapped[datetime] = mapped_column(comment='结束时间')
    success_count: Mapped[int] = mapped_column(
        INT, nullable=False, default=0, comment='成功数量'
    )
    error_count: Mapped[int] = mapped_column(
        INT, nullable=False, default=0, comment='错误数量'
    )
    failed_count: Mapped[int] = mapped_column(
        INT, nullable=False, default=0, comment='失败数量'
    )
    skipped_count: Mapped[int] = mapped_column(
        INT, nullable=False, default=0, comment='跳过数量'
    )
    status: Mapped[int] = mapped_column(
        SMALLINT,
        nullable=False,
        comment='执行状态0: pending, 1: running, 2: stopped, 3: finished',
        index=True,
    )
    mode: Mapped[int] = mapped_column(
        SMALLINT,
        default=0,
        comment='case执行模式0: 普通, 1: 测试集, 2: pipeline, 3: 其他',
    )
