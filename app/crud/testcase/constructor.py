#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/13 23:41
@Author   : wiesZheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.models.constructor import Constructor


class ConstructorCRUD(BaseCRUD):
    __model__ = Constructor

    pass
