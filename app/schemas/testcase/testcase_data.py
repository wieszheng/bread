# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/12 10:43
@Author   : wiesZheng
@Software : PyCharm
"""

from pydantic import BaseModel


class TestcaseDataParam(BaseModel):
    id: int = None
    case_id: int = None
    name: str
    json_data: str
    env: int
