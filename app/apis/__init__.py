# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:54
@Author   : wiesZheng
@Software : PyCharm
"""


# class Permission:
#     def __init__(self, role: int = Settings.MEMBER):
#         self.role = role
#
#     async def __call__(self, token: str = Header(...)):
#         if not token:
#             ...
#         try:
#             user_info = jwt_decode(token)
#
#             if user_info.get("role", 0) < self.role:
#                 raise AppExceptionNew(ExceptionEnum.Forbidden_ERROR)
#             async with async_session() as session:
#                 user = await user_crud.get_by_id(session, user_info.get("id"))
#             if user is None:
#                 raise AppExceptionNew(ExceptionEnum.USER_LOCK_ERROR)
#         except ExpiredSignatureError:
#             raise AppExceptionNew(ExceptionEnum.ExpiredSignature_ERROR)
#         except InvalidTokenError:
#             raise AppExceptionNew(ExceptionEnum.InvalidToken_ERROR)
#         user_info = model_to_dict(user, "password")
#         return user_info
