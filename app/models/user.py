# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:36
@Author   : wiesZheng
@Software : PyCharm
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class User(BaseModel):
    """
    用户信息表
    """

    __tablename__ = "bread_user"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID"
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, comment="用户名，用于登录"
    )
    nickname: Mapped[str] = mapped_column(
        String(50), index=True, comment="昵称，用于显示"
    )
    password: Mapped[str] = mapped_column(String(180), comment="密码，存储为哈希值")
    phone: Mapped[Optional[str]] = mapped_column(
        String(21), unique=True, comment="手机号码，唯一"
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, comment="电子邮箱，唯一"
    )
    avatar: Mapped[Optional[str]] = mapped_column(String(255), comment="头像链接或路径")
    role: Mapped[int] = mapped_column(
        default=0, comment="0: 普通用户 1: 组长 2: 超级管理员"
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, comment="最后登录时间"
    )
    is_valid: Mapped[bool] = mapped_column(
        Boolean, default=True, comment="账户是否有效，默认为True"
    )
