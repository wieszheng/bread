#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/17 22:02
@Author   : wiesZheng
@Software : PyCharm
"""

from typing import List

from pydantic import BaseModel


class TestcaseDirectoryParams(BaseModel):
    name: str
    project_id: int
    parent: int = None


class UpdateTestcaseDirectoryParams(TestcaseDirectoryParams):
    id: int


class MoveTestCaseParams(BaseModel):
    project_id: int
    id_list: List[int]
    directory_id: int
