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

from fastapi import Depends, File, Path, Query, UploadFile

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.core.client.miNio import minio_client
from app.core.security.Jwt import get_current_user_new
from app.crud.helper import compute_offset
from app.crud.project.project import ProjectCRUD, ProjectRoleCRUD
from app.exceptions.errors import CustomException
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.models.user import User
from app.schemas.auth.user import CurrentUserInfo, UserInfoSchemaBase
from app.schemas.project.project import (
    ProjectRoleParam,
    ProjectSchemaBase,
    UpdateProjectParam,
    UpdateProjectRoleParam,
)
from config import settings


class ProjectService:
    @staticmethod
    async def get_projects(
        current: Annotated[int, Query(..., ge=1, description='Page number')] = 1,
        pageSize: Annotated[
            int, Query(..., gt=0, le=100, description='Page size')
        ] = 10,
        name: Annotated[str | None, Query(description='项目名称')] = None,
    ) -> ResponseModel:
        filter_params = {}
        if name:
            filter_params = {'name': name}

        result = await ProjectCRUD.get_multi_joined(
            limit=pageSize,
            offset=compute_offset(current, pageSize),
            sort_columns='id',
            sort_orders='desc',
            join_model=User,
            join_prefix='user_',
            join_schema_to_select=UserInfoSchemaBase,
            is_deleted=False,
            join_on=Project.owner == User.id,
            **filter_params,
        )
        return await ResponseBase.success(
            result={**result, 'current': current, 'pageSize': pageSize}
        )

    @staticmethod
    async def get_project(project_id: Annotated[str, ...]) -> ResponseModel:
        input_id = await ProjectCRUD.get_joined(
            join_model=User,
            join_prefix='user_',
            join_schema_to_select=UserInfoSchemaBase,
            join_on=Project.owner == User.id,
            id=project_id,
            is_deleted=False,
        )
        if not input_id:
            raise CustomException(CustomErrorCode.PROJECT_ID_EXIST)
        roles = await ProjectRoleCRUD.get_multi_joined(
            limit=100,
            offset=compute_offset(1, 100),
            project_id=project_id,
            join_model=User,
            join_prefix='user_',
            join_schema_to_select=UserInfoSchemaBase,
            join_on=ProjectRole.user_id == User.id,
            return_total_count=False,
            is_deleted=False,
        )

        return await ResponseBase.success(
            result={'project': input_id, 'roles': roles['data']}
        )

    @staticmethod
    async def create_project(
        obj: ProjectSchemaBase,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        """
        创建项目
        :return:
        """
        input_name = await ProjectCRUD.exists(name=obj.name)
        if input_name:
            raise CustomException(CustomErrorCode.PROJECT_NAME_EXIST)
        result = await ProjectCRUD.create(obj=obj, created_by=user_info.id)
        return await ResponseBase.success(result=result.to_dict())

    @staticmethod
    async def update_project(
        obj: UpdateProjectParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        """
        更新项目
        :return:
        """
        input_id = await ProjectCRUD.get(id=obj.id)
        if not input_id:
            raise CustomException(CustomErrorCode.PROJECT_ID_EXIST)
        if input_id['owner'] != user_info.id and user_info.role < settings.ADMIN:
            raise CustomException(CustomErrorCode.PROJECT_No_PERMISSION)
        await ProjectCRUD.update(
            obj={**obj.model_dump(), 'updated_by': user_info.id},
            id=obj.id,
        )
        return await ResponseBase.success()

    @staticmethod
    async def update_project_avatar(
        project_id: Annotated[str, Path(...)],
        avatar: Annotated[UploadFile, File(..., description='上传的头像文件')],
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        """
        更新项目头像
        :return:
        """
        # 生成随机文件名
        input_id = await ProjectCRUD.get(id=project_id)
        if not input_id:
            raise CustomException(CustomErrorCode.PROJECT_ID_EXIST)
        if input_id['owner'] != user_info.id and user_info.role < settings.ADMIN:
            raise CustomException(CustomErrorCode.PROJECT_No_PERMISSION)
        random_suffix = str(uuid.uuid4()).replace('-', '')
        object_name = f"{user_info.id}/{random_suffix}.{avatar.filename.split('.')[-1]}"
        minio_client.upload_file(
            object_name, avatar.file, content_type=avatar.content_type
        )

        avatar_url = minio_client.pre_signature_get_object_url(object_name)
        await ProjectCRUD.update(
            obj={'avatar': avatar_url.split('?', 1)[0], 'updated_by': user_info.id},
            id=project_id,
        )

        return await ResponseBase.success(
            result={'avatar': avatar_url.split('?', 1)[0]}
        )

    @staticmethod
    async def delete_project(
        project_id: Annotated[int, ...],
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        input_id = await ProjectCRUD.get(id=project_id)
        if not input_id:
            raise CustomException(CustomErrorCode.PROJECT_ID_EXIST)
        if input_id['owner'] != user_info.id and user_info.role != settings.ADMIN:
            raise CustomException(CustomErrorCode.PROJECT_No_PERMISSION)
        await ProjectCRUD.delete(id=project_id)
        return await ResponseBase.success()

    @staticmethod
    async def allocation_project_role(
        obj: ProjectRoleParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        result = await ProjectRoleCRUD.exists(
            user_id=obj.user_id,
            project_id=obj.project_id,
            is_deleted=False,
        )
        if result:
            raise CustomException(CustomErrorCode.PROJECT_ROLE_EXIST)

        if user_info.role != settings.ADMIN:
            input_id = await ProjectCRUD.get(id=obj.project_id)
            if not input_id:
                raise CustomException(CustomErrorCode.PROJECT_ID_EXIST)

            if input_id['owner'] != user_info.id:
                if False and obj.project_role == settings.MANAGER:
                    raise CustomException(CustomErrorCode.PROJECT_No_LEADER)
            result = await ProjectRoleCRUD.get(
                user_id=obj.user_id, project_id=obj.project_id, is_deleted=False
            )
            if result is None or result['project_role'] == settings.MANAGER:
                raise CustomException(CustomErrorCode.PROJECT_No_PERMISSION)
        await ProjectRoleCRUD.create(obj=obj, created_by=user_info.id)

        return await ResponseBase.success()

    @staticmethod
    async def update_project_role(
        obj: UpdateProjectRoleParam,
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        result = await ProjectRoleCRUD.get(id=obj.id, is_deleted=False)
        if result is None:
            raise CustomException(CustomErrorCode.PROJECT_ROLE_NOT_EXIST)
        if user_info.role != settings.ADMIN:
            input_id = await ProjectCRUD.get(id=obj.project_id)
            if not input_id:
                raise CustomException(CustomErrorCode.PROJECT_ID_EXIST)

            if input_id['owner'] != user_info.id:
                if False and obj.project_role == settings.MANAGER:
                    raise CustomException(CustomErrorCode.PROJECT_No_LEADER)
            result = await ProjectRoleCRUD.get(
                user_id=obj.user_id, project_id=obj.project_id, is_deleted=False
            )
            if result is None or result['project_role'] == settings.MANAGER:
                raise CustomException(CustomErrorCode.PROJECT_No_PERMISSION)
        await ProjectRoleCRUD.update(
            obj={**obj.model_dump(), 'updated_by': user_info.id}, id=obj.id
        )
        return await ResponseBase.success()

    @staticmethod
    async def del_project_role(
        role_id: Annotated[int, ...],
        user_info: Annotated[CurrentUserInfo, Depends(get_current_user_new)],
    ) -> ResponseModel:
        result = await ProjectRoleCRUD.get(id=role_id, is_deleted=False)
        if result is None:
            raise CustomException(CustomErrorCode.PROJECT_ROLE_NOT_EXIST)
        if user_info.role != settings.ADMIN:
            input_id = await ProjectCRUD.get(id=result['project_id'])
            if not input_id:
                raise CustomException(CustomErrorCode.PROJECT_ID_EXIST)

            if input_id['owner'] != user_info.id:
                if False and result['project_role'] == settings.MANAGER:
                    raise CustomException(CustomErrorCode.PROJECT_No_LEADER)
            result = await ProjectRoleCRUD.get(
                user_id=result['user_id'],
                project_id=result['project_id'],
                is_deleted=False,
            )
            if result is None or result['project_role'] == settings.MANAGER:
                raise CustomException(CustomErrorCode.PROJECT_No_PERMISSION)

        await ProjectRoleCRUD.delete(id=role_id)
        return await ResponseBase.success()
