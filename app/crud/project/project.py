#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/22 23:26
@Author   : wiesZheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.models.project import Project
from app.models.project_role import ProjectRole


class ProjectCRUD(BaseCRUD):
    __model__ = Project

    pass


class ProjectRoleCRUD(BaseCRUD):
    __model__ = ProjectRole
    pass
