# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 17:36
@Author   : wiesZheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.enums.exception import ErrorCodeEnum
from app.exceptions.exception import BusinessException
from app.models.user import SysUser
from app.schemas.user import AddUser, UserRegisterIn
from app.service.login_s import LoginService


class UserCRUD(BaseCRUD):
    __model__ = SysUser

    @classmethod
    async def get_user_by_name(cls, user_name: str):
        """
        根据用户名获取用户信息
        :param user_name: 用户名
        :return: 当前用户名的用户信息对象
        """
        query_user_info = await cls.exists(username=user_name)

        return query_user_info

    @classmethod
    async def verify_user_register_info(cls, user_item: UserRegisterIn):
        """ 校验用户注册信息 """
        # 校验用户名是否存在
        result = await cls.exists(username=user_item.username)
        if result:
            raise BusinessException(ErrorCodeEnum.ACCOUNT_ERR)

        # 校验手机号是否存在
        result = await cls.exists(phone=user_item.phone)
        if result:
            raise BusinessException(ErrorCodeEnum.MOBILE_ERR)

    @classmethod
    async def user_register(cls, user_item: UserRegisterIn):
        await cls.verify_user_register_info(user_item)
        # 创建注册用户
        user = await cls.create(obj=user_item)
        current_user = user.to_dict("password")
        # 注册成功则保存登录状态，签发token
        token = await LoginService.create_access_token(current_user)
        return current_user, token
