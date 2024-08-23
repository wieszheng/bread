#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/22 23:16
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import File, UploadFile
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.commons.schema import PersistentDeletion, TimestampSchema


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
    model_config = ConfigDict(from_attributes=True)
    id: int


class GetProjectInfo(ProjectSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_by: int | None = None


class GetCurrentProjectInfoDetail(GetProjectInfo, TimestampSchema, PersistentDeletion):
    pass
