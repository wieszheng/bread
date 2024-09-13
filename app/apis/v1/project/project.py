#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/22 22:52
@Author   : wiesZheng
@Software : PyCharm
"""

from fastapi import APIRouter, Depends

from app.core.security.Jwt import DependsJwtAuth
from app.core.security.permission import Permission
from app.service.project.project import ProjectService
from config import settings

router = APIRouter(prefix='/project', tags=['项目管理'], dependencies=[DependsJwtAuth])

router.add_api_route(
    '/list',
    endpoint=ProjectService.get_projects,
    methods=['get'],
    summary='（支持条件）分页获取所有项目',
)

router.add_api_route(
    '',
    endpoint=ProjectService.get_project,
    methods=['get'],
    summary='Id查询项目',
)

router.add_api_route(
    '',
    endpoint=ProjectService.create_project,
    dependencies=[Depends(Permission(settings.ADMIN))],
    methods=['post'],
    summary='新增项目',
)

router.add_api_route(
    '',
    endpoint=ProjectService.update_project,
    dependencies=[Depends(Permission(settings.ADMIN))],
    methods=['put'],
    summary='修改项目',
)

router.add_api_route(
    '/avatar/{project_id}',
    endpoint=ProjectService.update_project_avatar,
    dependencies=[Depends(Permission(settings.ADMIN))],
    methods=['put'],
    summary='修改项目头像',
)

router.add_api_route(
    '',
    endpoint=ProjectService.delete_project,
    dependencies=[Depends(Permission(settings.ADMIN))],
    methods=['delete'],
    summary='删除项目（逻辑删除）',
)

router.add_api_route(
    '/role',
    endpoint=ProjectService.allocation_project_role,
    dependencies=[Depends(Permission(settings.MANAGER))],
    methods=['post'],
    summary='分配项目角色',
)

router.add_api_route(
    '/role',
    endpoint=ProjectService.update_project_role,
    dependencies=[Depends(Permission(settings.MANAGER))],
    methods=['put'],
    summary='修改项目角色',
)

router.add_api_route(
    '/role',
    endpoint=ProjectService.del_project_role,
    dependencies=[Depends(Permission(settings.MANAGER))],
    methods=['delete'],
    summary='删除项目角色',
)
