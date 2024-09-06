#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/22 23:16
@Author   : wiesZheng
@Software : PyCharm
"""
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from app.commons.response.response_schema import ListPageRequestModel


class ProjectSchemaBase(BaseModel):
    name: str = Field(..., description="项目名称")
    app: str = Field(..., description="项目所属应用")
    owner: int = Field(..., description="项目拥有者")
    private: bool = False
    description: str = "这是一个项目简介。"
    dingtalk_url: str = None

    @field_validator("name")
    def validate_username(cls, value: str):
        if 2 > len(value) > 6:
            raise ValueError("项目名称不能小于2大于6个字符")
        return value


class UpdateProjectParam(ProjectSchemaBase):
    id: int


class GetProjectInfo(ProjectSchemaBase):
    # avatar: str | None = None
    pass


class ProjectListIn(ListPageRequestModel):
    page: int = Field(default=1, ge=0, description="分页偏移量")
    page_size: int = Field(default=10, gt=0, description="每页显示数量")
    orderings: Optional[List[str]] = Field(default=["id"], description="排序字段")


class ProjectRoleParam(BaseModel):
    user_id: int
    project_role: int
    project_id: int


class UpdateProjectRoleParam(ProjectRoleParam):
    id: int
