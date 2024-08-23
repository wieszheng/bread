#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/22 22:55
@Author   : wiesZheng
@Software : PyCharm
"""
import uuid
from typing import Annotated

from fastapi import File, Path, Request, UploadFile

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.core.client.miNio import minio_client
from app.crud.project.project import ProjectCRUD
from app.exceptions.errors import CustomException
from app.schemas.project.project import (
    GetProjectInfo,
    ProjectSchemaBase,
    UpdateProjectParam,
)


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
        if obj.owner:
            obj.owner = request.user.id
        project_data = await ProjectCRUD.create(obj=obj, created_by=request.user.id)
        data = GetProjectInfo.model_validate(project_data).model_dump()
        return await ResponseBase.success(result=data)

    @staticmethod
    async def update_project(
        request: Request, obj: UpdateProjectParam
    ) -> ResponseModel:
        """
        更新项目
        :param request:
        :param obj:
        :return:
        """
        pass

    @staticmethod
    async def update_project_avatar(
        request: Request,
        project_id: Annotated[str, Path(...)],
        avatar: UploadFile = File(..., description="上传的头像文件"),
    ) -> ResponseModel:
        """
        更新项目头像
        :param request:
        :param project_id:
        :param avatar:
        :return:
        """
        # 生成随机文件名
        input_id = await ProjectCRUD.exists(id=project_id)
        if not input_id:
            raise CustomException(CustomErrorCode.PROJECT_ID_EXIST)
        random_suffix = str(uuid.uuid4()).replace("-", "")
        object_name = (
            f"{request.user.id}/{random_suffix}.{avatar.filename.split('.')[-1]}"
        )
        minio_client.upload_file(
            object_name, avatar.file, content_type=avatar.content_type
        )

        avatar_url = minio_client.pre_signature_get_object_url(object_name)
        await ProjectCRUD.update(
            obj={"avatar": avatar_url.split("?", 1)[0], "updated_by": request.user.id},
            id=project_id,
        )

        return await ResponseBase.success()

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
