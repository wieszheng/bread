#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 23:38
@Author   : wiesZheng
@Software : PyCharm
"""

from pydantic import BaseModel, Field

from app.commons.enums import KeyType


class GlobalConfigSchemaBase(BaseModel):
    key: str = Field(..., description="配置键值")
    value: str = Field(..., description="配置值")
    env: str | None = None
    key_type: KeyType = Field(..., description="配置类型")
    enable: bool = Field(..., description="是否弃用")
