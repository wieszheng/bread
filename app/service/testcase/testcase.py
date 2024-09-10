#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 0:06
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import Depends

from app.commons.response.response_code import CustomErrorCode
from app.commons.response.response_schema import ResponseBase, ResponseModel
from app.core.security.Jwt import get_current_user_new
from app.crud.testcase.testcase import TestCaseCRUD
from app.exceptions.errors import CustomException
from app.schemas.auth.user import CurrentUserInfo
from app.schemas.testcase.testcase import TestCaseParam, TestCaseSchemaBase


class TestCaseService:

    @staticmethod
    async def get_testcase_list(id: int):
        pass

    @staticmethod
    async def add_testcase(
        obj: TestCaseSchemaBase,
        user_info: CurrentUserInfo = Depends(get_current_user_new),
    ) -> ResponseModel:
        input_ = await TestCaseCRUD.exists(name=obj.name, directory_id=obj.directory_id)
        if not input_:
            raise CustomException(CustomErrorCode.CASE_NAME_EXIST)
        model = TestCaseCRUD.__model__(obj.model_dump_json(), created_by=user_info.id)
        await TestCaseCRUD.create(obj=model)
        return await ResponseBase.success()

    @staticmethod
    async def create_testcase(id: int):
        pass

    @staticmethod
    async def update_testcase(id: int):
        pass

    @staticmethod
    async def delete_testcase(id: int):
        pass

    @staticmethod
    async def get_testcase(id: int):
        pass

    @staticmethod
    async def get_xmind(id: int):
        pass

    @staticmethod
    async def move_testcase(id: int):
        pass

    @staticmethod
    async def get_record_start(id: int):
        pass

    @staticmethod
    async def get_record_stop(id: int):
        pass

    @staticmethod
    async def get_record_status(id: int):
        pass

    @staticmethod
    async def get_record_remove(id: int):
        pass

    @staticmethod
    async def create_generate(id: int):
        pass

    @staticmethod
    async def testcase_import(id: int):
        pass

    @staticmethod
    async def get_variables(id: int):
        pass
