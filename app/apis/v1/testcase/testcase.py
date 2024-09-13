#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/9/10 0:05
@Author   : wiesZheng
@Software : PyCharm
"""

from fastapi import APIRouter, Depends

from app.core.security.Jwt import DependsJwtAuth
from app.core.security.permission import Permission
from app.service.testcase.constructor import ConstructorService
from app.service.testcase.test_report import TestReportService
from app.service.testcase.testcase import TestCaseService
from app.service.testcase.testcase_asserts import TestCaseAssertsService
from app.service.testcase.testcase_data import TestcaseDataService
from app.service.testcase.testcase_directory import TestcaseDirectoryService
from app.service.testcase.testcase_out_parameters import TestCaseOutParametersService

router = APIRouter(prefix='/testcase', tags=['用例管理'], dependencies=[DependsJwtAuth])

router.add_api_route(
    '/list',
    endpoint=TestCaseService.get_testcase_list,
    methods=['get'],
    summary='（支持条件）获取所有用例',
    dependencies=[Depends(Permission(2))],
)

router.add_api_route(
    '', endpoint=TestCaseService.add_testcase, methods=['post'], summary='添加用例 v1'
)

router.add_api_route(
    '/create',
    endpoint=TestCaseService.create_testcase,
    methods=['post'],
    summary='创建接口测试用例 v2 支持多参数',
)

router.add_api_route(
    '',
    endpoint=TestCaseService.update_testcase,
    methods=['put'],
    summary='修改用例',
)

router.add_api_route(
    '',
    endpoint=TestCaseService.delete_testcase,
    methods=['delete'],
    summary='删除用例',
)

router.add_api_route(
    '',
    endpoint=TestCaseService.get_testcase,
    methods=['get'],
    summary='查询单条用例信息',
)

router.add_api_route(
    '/asserts',
    endpoint=TestCaseAssertsService.create_asserts,
    methods=['post'],
    summary='创建用例断言信息',
)

router.add_api_route(
    '/asserts',
    endpoint=TestCaseAssertsService.update_asserts,
    methods=['put'],
    summary='修改用例断言信息',
)

router.add_api_route(
    '/asserts',
    endpoint=TestCaseAssertsService.delete_asserts,
    methods=['delete'],
    summary='删除用例断言信息',
)

router.add_api_route(
    '/constructor',
    endpoint=ConstructorService.create_constructor,
    methods=['post'],
    summary='新建前置条件构造器',
)

router.add_api_route(
    '/constructor',
    endpoint=ConstructorService.update_constructor,
    methods=['put'],
    summary='修改前置条件构造器',
)

router.add_api_route(
    '/constructor',
    endpoint=ConstructorService.delete_constructor,
    methods=['delete'],
    summary='删除前置条件构造器',
)

router.add_api_route(
    '/constructor',
    endpoint=ConstructorService.get_constructor,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/constructors',
    endpoint=ConstructorService.get_constructor_list,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/constructor/order',
    endpoint=ConstructorService.update_constructor_order,
    methods=['put'],
    summary='',
)

router.add_api_route(
    '/constructor/tree',
    endpoint=ConstructorService.get_constructor_tree,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/report',
    endpoint=TestReportService.get_report,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/reports',
    endpoint=TestReportService.get_report_list,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/xmind',
    endpoint=TestCaseService.get_xmind,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/directory',
    endpoint=TestcaseDirectoryService.get_directory,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/tree',
    endpoint=TestcaseDirectoryService.get_tree,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/directory',
    endpoint=TestcaseDirectoryService.get_directory,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/directory',
    endpoint=TestcaseDirectoryService.create_directory,
    methods=['post'],
    summary='',
)

router.add_api_route(
    '/directory',
    endpoint=TestcaseDirectoryService.update_directory,
    methods=['put'],
    summary='',
)

router.add_api_route(
    '/directory',
    endpoint=TestcaseDirectoryService.delete_directory,
    methods=['delete'],
    summary='',
)

router.add_api_route(
    '/data',
    endpoint=TestcaseDataService.create_data,
    methods=['post'],
    summary='',
)

router.add_api_route(
    '/data',
    endpoint=TestcaseDataService.update_data,
    methods=['put'],
    summary='',
)

router.add_api_route(
    '/data',
    endpoint=TestcaseDataService.delete_data,
    methods=['delete'],
    summary='',
)

router.add_api_route(
    '/move',
    endpoint=TestCaseService.move_testcase,
    methods=['post'],
    summary='',
)

router.add_api_route(
    '/parameters',
    endpoint=TestCaseOutParametersService.create_parameters,
    methods=['post'],
    summary='',
)

router.add_api_route(
    '/parameters',
    endpoint=TestCaseOutParametersService.update_parameters,
    methods=['put'],
    summary='',
)

router.add_api_route(
    '/parameters',
    endpoint=TestCaseOutParametersService.delete_parameters,
    methods=['delete'],
    summary='',
)

router.add_api_route(
    '/parameters/batch',
    endpoint=TestCaseOutParametersService.update_parameters_batch,
    methods=['put'],
    summary='',
)

router.add_api_route(
    '/record/start',
    endpoint=TestCaseService.get_record_start,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/record/stop',
    endpoint=TestCaseService.get_record_stop,
    methods=['get'],
    summary='',
)
router.add_api_route(
    '/record/status',
    endpoint=TestCaseService.get_record_status,
    methods=['get'],
    summary='',
)
router.add_api_route(
    '/record/remove',
    endpoint=TestCaseService.get_record_remove,
    methods=['get'],
    summary='',
)

router.add_api_route(
    '/generate',
    endpoint=TestCaseService.create_generate,
    methods=['post'],
    summary='',
)

router.add_api_route(
    '/import',
    endpoint=TestCaseService.testcase_import,
    methods=['post'],
    summary='',
)
router.add_api_route(
    '/variables',
    endpoint=TestCaseService.get_variables,
    methods=['post'],
    summary='',
)
