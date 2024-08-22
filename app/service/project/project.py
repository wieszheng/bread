#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/22 22:55
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import Request

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.crud.project.project import ProjectCRUD
from app.exceptions.errors import CustomException
from app.schemas.project.project import GetProjectInfo, ProjectSchemaBase


class ProjectService:

    @staticmethod
    async def get_projects():
        pass

    @staticmethod
    async def create_project(request: Request, obj: ProjectSchemaBase) -> ResponseModel:
        """
        创建项目
        :return:
        """
        input_name = await ProjectCRUD.exists(name=obj.name)
        if input_name:
            raise CustomException(CustomErrorCode.PROJECT_NAME_EXIST)
        obj.owner = request.user.id
        project_data = await ProjectCRUD.create(obj=obj, created_by=request.user.id)
        data = GetProjectInfo.model_validate(project_data).model_dump()
        return await ResponseBase.success(result=data)

    @staticmethod
    async def update_project():
        pass

    @staticmethod
    async def update_project_avatar():
        pass

    @staticmethod
    async def is_del_project():
        pass

    @staticmethod
    async def allocation_project_role():
        pass

    @staticmethod
    async def update_project_role():
        pass

    @staticmethod
    async def del_project_role():
        pass
