# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/16 10:48
@Author   : wiesZheng
@Software : PyCharm
"""

from fastapi import Depends

from app.core.security.Jwt import get_current_user_new
from app.exceptions.errors import PermissionException
from app.schemas.auth.user import CurrentUserInfo
from config import settings


class Permission:
    def __init__(self, role: int = settings.MEMBER):
        self.role = role

    async def __call__(
        self, current_user: CurrentUserInfo = Depends(get_current_user_new)
    ):
        if current_user.role < self.role:
            raise PermissionException(message='该用户无此接口权限')
        return True


# class CheckUserInterfaceAuth:
#     """
#     校验当前用户是否具有相应的接口权限
#     :param perm: 权限标识
#     :param is_strict: 当传入的权限标识是list类型时，是否开启严格模式，开启表示会校验列表中的每一个权限标识，所有的校验结果都需要为True才会通过
#     """
#     def __init__(self, perm: Union[str, List], is_strict: bool = False):
#         self.perm = perm
#         self.is_strict = is_strict
#
#     def __call__(self, current_user: CurrentUserInfo = Depends(get_current_user)):
#         user_auth_list = [item.perms for item in current_user.menu]
#         user_auth_list.append('common')
#         if isinstance(self.perm, str):
#             if self.perm in user_auth_list:
#                 return True
#         if isinstance(self.perm, list):
#             if self.is_strict:
#                 if all([perm_str in user_auth_list for perm_str in self.perm]):
#                     return True
#             else:
#                 if any([perm_str in user_auth_list for perm_str in self.perm]):
#                     return True
#         raise PermissionException(data="", message="该用户无此接口权限")


# class CheckRoleInterfaceAuth:
#     """
#     根据角色校验当前用户是否具有相应的接口权限
#     :param role_key: 角色标识
#     :param is_strict: 当传入的角色标识是list类型时，是否开启严格模式，开启表示会校验列表中的每一个角色标识，所有的校验结果都需要为True才会通过
#     """
#     def __init__(self, role_key: Union[str, List], is_strict: bool = False):
#         self.role_key = role_key
#         self.is_strict = is_strict
#
#     def __call__(self, current_user: CurrentUserInfo = Depends(get_current_user)):
#         user_role_list = current_user.role
#         user_role_key_list = [role.role_key for role in user_role_list]
#         if isinstance(self.role_key, str):
#             if self.role_key in user_role_key_list:
#                 return True
#         if isinstance(self.role_key, list):
#             if self.is_strict:
#                 if all([role_key_str in user_role_key_list for role_key_str in self.role_key]):
#                     return True
#             else:
#                 if any([role_key_str in user_role_key_list for role_key_str in self.role_key]):
#                     return True
#         raise PermissionException(data="", message="该用户无此接口权限")
