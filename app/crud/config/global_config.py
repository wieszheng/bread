# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 14:53
@Author   : wiesZheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.models.global_config import GlobalConfig


class GlobalConfigCRUD(BaseCRUD):
    __model__ = GlobalConfig

    pass
