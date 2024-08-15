# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 11:51
@Author   : wiesZheng
@Software : PyCharm
"""
from enum import Enum


class BaseEnum(Enum):
    """枚举基类"""

    @classmethod
    def get_member_values(cls):
        return [item.value for item in cls._member_map_.values()]

    @classmethod
    def get_member_names(cls):
        return [name for name in cls._member_names_]


class StatusCodeEnum(BaseEnum):
    """ 错误码枚举类 """

    OK = (0, '成功')
    ERROR = (-1, '错误')
    SERVER_ERR = (500, '服务器异常')

    IMAGE_CODE_ERR = (4001, '图形验证码错误')
    THROTTLING_ERR = (4002, '访问过于频繁')
    NECESSARY_PARAM_ERR = (4003, '缺少必传参数')
    USER_ERR = (4004, '用户名错误')
    PWD_ERR = (4005, '密码错误')
    CP_PWD_ERR = (4006, '密码不一致')
    MOBILE_ERR = (4007, '手机号错误')
    SMS_CODE_ERR = (4008, '短信验证码有误')
    ALLOW_ERR = (4009, '未勾选协议')
    SESSION_ERR = (4010, '用户未登录')

    DB_ERR = (5000, '数据错误')
    EMAIL_ERR = (5001, '邮箱错误')
    TEL_ERR = (5002, '固定电话错误')
    NODATA_ERR = (5003, '无数据')
    NEW_PWD_ERR = (5004, '新密码错误')
    OPENID_ERR = (5005, '无效的openid')
    PARAM_ERR = (5006, '参数错误')
    STOCK_ERR = (5007, '库存不足')

    # 业务状态码
    PARTNER_CODE_OK = (0, "OK")
    PARTNER_CODE_FAIL = (-1, "操作失败")

    # 10000 - 11000 账号体系
    WRONG_USER_NAME_OR_PASSWORD = (10001, "账号或者密码错误！😱")  # 账号或密码错误
    PARTNER_CODE_EMPLOYEE_FAIL = (10002, "账号错误！")  # 账号错误
    WRONG_USER_NAME_OR_PASSWORD_LOCK = (10003, "密码输入错误超过次数，请5分钟后再登录！😭")
    USERNAME_OR_EMAIL_IS_REGISTER = (10004, "用户名已被注册")
    USER_EMAIL_OR_EMAIL_IS_REGISTER = (10004, "邮箱已被注册")
    USER_ID_IS_NULL = (10005, "用户id不能为空")
    PASSWORD_TWICE_IS_NOT_AGREEMENT = (10006, "两次输入的密码不一致")
    NEW_PWD_NO_OLD_PWD_EQUAL = (10007, "新密码不能与旧密码相同")
    OLD_PASSWORD_ERROR = (10008, "旧密码错误")

    # 用户状态 验证  11000 - 12000
    PARTNER_CODE_TOKEN_EXPIRED_FAIL = (11000, "用户信息以已过期 😂")  # token已过期

    # 参数类型 12000 - 13000
    PARTNER_CODE_PARAMS_FAIL = (12000, "必填参数不能为空 😅")  # 必填参数不能为空

    # project 项目 13000 - 14000
    PROJECT_HAS_MODULE_ASSOCIATION = (13000, "项目有模块或用例关联，不能删除")
    PROJECT_NAME_EXIST = (13001, "项目名已存在")  # 项目名以存在

    # module 模块 14000 - 15000
    MODULE_HAS_CASE_ASSOCIATION = (14000, " 模块有用例关联, 请删除对于模块下的用例")  # 模块有用例关联
    MODULE_NAME_EXIST = (14001, "模块名已存在")  # 模块名以存在

    @property
    def code(self):
        """ 获取错误码 """
        return self.value[0]

    @property
    def msg(self):
        """ 获取错误码码信息 """
        return self.value[1]
