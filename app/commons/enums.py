#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/17 11:24
@Author   : wiesZheng
@Software : PyCharm
"""
import enum


class RoleType(enum.IntEnum):
    """权限"""

    MEMBER = 0
    MANAGER = 1
    ADMIN = 2
