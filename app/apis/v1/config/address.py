# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/27 14:58
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import APIRouter

from app.core.security.Jwt import DependsJwtAuth
from app.service.config.address import AddressService

router = APIRouter(
    prefix="/config/address", tags=["网关地址配置"], dependencies=[DependsJwtAuth]
)

router.add_api_route(
    "",
    endpoint=AddressService.create_address,
    methods=["post"],
    summary="新增网关地址",
)

router.add_api_route(
    "",
    endpoint=AddressService.get_address,
    methods=["get"],
    summary="查询网关地址",
)

router.add_api_route(
    "",
    endpoint=AddressService.delete_address,
    methods=["delete"],
    summary="删除网关地址",
)

router.add_api_route(
    "",
    endpoint=AddressService.update_address,
    methods=["put"],
    summary="修改网关地址",
)

router.add_api_route(
    "/list",
    endpoint=AddressService.get_address_list,
    methods=["get"],
    summary="获取网关地址（支持条件查询）",
)
