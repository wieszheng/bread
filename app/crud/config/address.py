# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 14:53
@Author   : wiesZheng
@Software : PyCharm
"""
from app.crud import BaseCRUD
from app.models.address import Address


class AddressCRUD(BaseCRUD):
    __model__ = Address

    pass
