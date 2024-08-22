#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/10 20:59
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import field_validator
from sqlalchemy.orm.util import AliasedClass


class JoinConfig(BaseModel):
    model: Any
    join_on: Any
    join_prefix: Optional[str] = None
    schema_to_select: Optional[type[BaseModel]] = None
    join_type: str = "left"
    alias: Optional[AliasedClass] = None
    filters: Optional[dict] = None
    relationship_type: Optional[str] = "one-to-one"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("relationship_type")
    def check_valid_relationship_type(cls, value):
        valid_relationship_types = {"one-to-one", "one-to-many"}
        if value is not None and value not in valid_relationship_types:
            raise ValueError(f"Invalid relationship type: {value}")  # pragma: no cover
        return value

    @field_validator("join_type")
    def check_valid_join_type(cls, value):
        valid_join_types = {"left", "inner"}
        if value not in valid_join_types:
            raise ValueError(f"Unsupported join type: {value}")
        return value


def compute_offset(page: int, items_per_page: int) -> int:
    """
    根据给定的页码和每页的项目数计算分页的偏移量。偏移量表示给定页面上的项目在数据集中的起点

    Args:
        page：当前页码。页码应从 1 开始。items_per_page：每个页面上要显示的项目数
    Returns:
        计算出的偏移量

    """
    return (page - 1) * items_per_page
