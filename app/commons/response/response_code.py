# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 11:51
@Author   : wiesZheng
@Software : PyCharm
"""
import dataclasses
from enum import Enum
from functools import lru_cache


class CustomCodeBase(Enum):
    """自定义状态码基类"""

    @classmethod
    def get_member_values(cls):
        return [item.value for item in cls._member_map_.values()]

    @classmethod
    def get_member_names(cls):
        return [name for name in cls._member_names_]

    @property
    def code(self) -> int:
        """获取错误码"""
        return self.value[0]

    @property
    def msg(self) -> str:
        """获取错误码码信息"""
        return self.value[1]

    @classmethod
    @lru_cache
    def get_code_msg_dict_cache(cls) -> dict[int, str]:
        """以缓存的方式返回响应状态码与响应信息的映射
        Returns:
            dict[int, str]: 响应状态码与响应信息的映射
        """
        return {item.code: item.msg for item in cls}

    @classmethod
    def use_code_get_enum_msg(cls, code: int) -> str:
        """通过响应状态码获取对应的响应信息
        Args:
            code: 响应状态码

        Returns:
            str: 响应信息
        """
        mapping = cls.get_code_msg_dict_cache()
        return mapping[code]


class CustomResponseCode(CustomCodeBase):
    """响应状态码"""

    HTTP_200 = (200, "请求成功")
    HTTP_201 = (201, "新建请求成功")
    HTTP_202 = (202, "请求已接受，但处理尚未完成")
    HTTP_204 = (204, "请求成功，但没有返回内容")
    HTTP_400 = (400, "错误的请求")
    HTTP_401 = (401, "未经许可授权")
    HTTP_403 = (403, "失败！当前访问没有权限，或操作的数据没权限!")
    HTTP_404 = (404, "请求的地址不存在")
    HTTP_405 = (405, "不允许使用此方法提交访问")
    HTTP_410 = (410, "请求的资源已永久删除")
    HTTP_422 = (422, "请求参数非法")
    HTTP_425 = (425, "无法执行请求，由于服务器无法满足要求")
    HTTP_429 = (429, "请求过多，服务器限制")
    HTTP_500 = (500, "服务器内部错误")
    HTTP_502 = (502, "网关错误")
    HTTP_503 = (503, "服务器暂时无法处理请求")
    HTTP_504 = (504, "网关超时")


class CustomErrorCode(CustomCodeBase):
    """错误码枚举类"""

    # 业务状态码
    PARTNER_CODE_OK = (0, "OK")
    PARTNER_CODE_FAIL = (-1, "操作失败")

    # 10000 - 11000 账号体系
    WRONG_USER_NAME_OR_PASSWORD = (10001, "账号或者密码错误！😱")  # 账号或密码错误
    PARTNER_CODE_EMPLOYEE_FAIL = (10002, "账号错误！")  # 账号错误
    WRONG_USER_NAME_OR_PASSWORD_LOCK = (
        10003,
        "密码输入错误超过次数，请5分钟后再登录！😭",
    )
    USERNAME_OR_EMAIL_IS_REGISTER = (10004, "用户名已被注册")
    NICKNAME_OR_EMAIL_IS_REGISTER = (10004, "昵称已被注册")
    USER_EMAIL_OR_EMAIL_IS_REGISTER = (10004, "邮箱已被注册")
    USER_ID_IS_NULL = (10005, "用户id不能为空")
    PASSWORD_TWICE_IS_NOT_AGREEMENT = (10006, "两次输入的密码不一致")
    NEW_PWD_NO_OLD_PWD_EQUAL = (10007, "新密码不能与旧密码相同")
    OLD_PASSWORD_ERROR = (10008, "旧密码错误")
    USER_ACCOUNT_LOCKED = (10009, "用户账号被锁定，请联系管理员 😭")
    USER_IS_ADMIN = (10010, "不可操作超级管理员")
    YOU_INFO = (10010, "只能修改自己的信息呦 👉")
    # 用户状态 验证  11000 - 12000
    PARTNER_CODE_TOKEN_EXPIRED_FAIL = (
        11000,
        "用户信息以已过期 😂",
    )  # token已过期或未找到

    # 参数类型 12000 - 13000
    PARTNER_CODE_PARAMS_FAIL = (12000, "必填参数不能为空 😅")  # 必填参数不能为空

    # 项目 13000 - 14000
    PROJECT_HAS_MODULE_ASSOCIATION = (13000, "项目有模块或用例关联，不能删除")
    PROJECT_No_PERMISSION = (13000, "你没有权限修改项目头像，请联系项目管理员 😭")
    PROJECT_NAME_EXIST = (13001, "项目名已存在")  # 项目名以存在
    PROJECT_ID_EXIST = (13001, "项目不存在，请确认")  # 项目不存在
    PROJECT_ROLE_EXIST = (13002, "该用户已存在")
    PROJECT_No_LEADER = (13002, "不能修改组长的权限")
    PROJECT_ROLE_NOT_EXIST = (13002, "该用户角色不存在")

    ENVIRONMENT_NAME_EXIST = (14000, "环境名已存在")
    ENVIRONMENT_ID_NOT_EXIST = (14001, "环境不存在,请检查")

    ADDRESS_NAME_EXIST = (14100, "网关名已存在")
    ADDRESS_ID_NOT_EXIST = (14101, "网关不存在,请检查")

    # module 模块 14000 - 15000
    MODULE_HAS_CASE_ASSOCIATION = (
        14000,
        " 模块有用例关联, 请删除对于模块下的用例",
    )  # 模块有用例关联
    MODULE_NAME_EXIST = (14001, "模块名已存在")  # 模块名以存在


class StandardResponseCode:
    """标准响应状态码"""

    """
    HTTP codes
    See HTTP Status Code Registry:
    https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

    And RFC 2324 - https://tools.ietf.org/html/rfc2324
    """
    HTTP_100 = 100  # CONTINUE: 继续
    HTTP_101 = 101  # SWITCHING_PROTOCOLS: 协议切换
    HTTP_102 = 102  # PROCESSING: 处理中
    HTTP_103 = 103  # EARLY_HINTS: 提示信息
    HTTP_200 = 200  # OK: 请求成功
    HTTP_201 = 201  # CREATED: 已创建
    HTTP_202 = 202  # ACCEPTED: 已接受
    HTTP_203 = 203  # NON_AUTHORITATIVE_INFORMATION: 非权威信息
    HTTP_204 = 204  # NO_CONTENT: 无内容
    HTTP_205 = 205  # RESET_CONTENT: 重置内容
    HTTP_206 = 206  # PARTIAL_CONTENT: 部分内容
    HTTP_207 = 207  # MULTI_STATUS: 多状态
    HTTP_208 = 208  # ALREADY_REPORTED: 已报告
    HTTP_226 = 226  # IM_USED: 使用了
    HTTP_300 = 300  # MULTIPLE_CHOICES: 多种选择
    HTTP_301 = 301  # MOVED_PERMANENTLY: 永久移动
    HTTP_302 = 302  # FOUND: 临时移动
    HTTP_303 = 303  # SEE_OTHER: 查看其他位置
    HTTP_304 = 304  # NOT_MODIFIED: 未修改
    HTTP_305 = 305  # USE_PROXY: 使用代理
    HTTP_307 = 307  # TEMPORARY_REDIRECT: 临时重定向
    HTTP_308 = 308  # PERMANENT_REDIRECT: 永久重定向
    HTTP_400 = 400  # BAD_REQUEST: 请求错误
    HTTP_401 = 401  # UNAUTHORIZED: 未授权
    HTTP_402 = 402  # PAYMENT_REQUIRED: 需要付款
    HTTP_403 = 403  # FORBIDDEN: 禁止访问
    HTTP_404 = 404  # NOT_FOUND: 未找到
    HTTP_405 = 405  # METHOD_NOT_ALLOWED: 方法不允许
    HTTP_406 = 406  # NOT_ACCEPTABLE: 不可接受
    HTTP_407 = 407  # PROXY_AUTHENTICATION_REQUIRED: 需要代理身份验证
    HTTP_408 = 408  # REQUEST_TIMEOUT: 请求超时
    HTTP_409 = 409  # CONFLICT: 冲突
    HTTP_410 = 410  # GONE: 已删除
    HTTP_411 = 411  # LENGTH_REQUIRED: 需要内容长度
    HTTP_412 = 412  # PRECONDITION_FAILED: 先决条件失败
    HTTP_413 = 413  # REQUEST_ENTITY_TOO_LARGE: 请求实体过大
    HTTP_414 = 414  # REQUEST_URI_TOO_LONG: 请求 URI 过长
    HTTP_415 = 415  # UNSUPPORTED_MEDIA_TYPE: 不支持的媒体类型
    HTTP_416 = 416  # REQUESTED_RANGE_NOT_SATISFIABLE: 请求范围不符合要求
    HTTP_417 = 417  # EXPECTATION_FAILED: 期望失败
    HTTP_418 = 418  # UNUSED: 闲置
    HTTP_421 = 421  # MISDIRECTED_REQUEST: 被错导的请求
    HTTP_422 = 422  # UNPROCESSABLE_CONTENT: 无法处理的实体
    HTTP_423 = 423  # LOCKED: 已锁定
    HTTP_424 = 424  # FAILED_DEPENDENCY: 依赖失败
    HTTP_425 = 425  # TOO_EARLY: 太早
    HTTP_426 = 426  # UPGRADE_REQUIRED: 需要升级
    HTTP_427 = 427  # UNASSIGNED: 未分配
    HTTP_428 = 428  # PRECONDITION_REQUIRED: 需要先决条件
    HTTP_429 = 429  # TOO_MANY_REQUESTS: 请求过多
    HTTP_430 = 430  # Unassigned: 未分配
    HTTP_431 = 431  # REQUEST_HEADER_FIELDS_TOO_LARGE: 请求头字段太大
    HTTP_451 = 451  # UNAVAILABLE_FOR_LEGAL_REASONS: 由于法律原因不可用
    HTTP_500 = 500  # INTERNAL_SERVER_ERROR: 服务器内部错误
    HTTP_501 = 501  # NOT_IMPLEMENTED: 未实现
    HTTP_502 = 502  # BAD_GATEWAY: 错误的网关
    HTTP_503 = 503  # SERVICE_UNAVAILABLE: 服务不可用
    HTTP_504 = 504  # GATEWAY_TIMEOUT: 网关超时
    HTTP_505 = 505  # HTTP_VERSION_NOT_SUPPORTED: HTTP 版本不支持
    HTTP_506 = 506  # VARIANT_ALSO_NEGOTIATES: 变体也会协商
    HTTP_507 = 507  # INSUFFICIENT_STORAGE: 存储空间不足
    HTTP_508 = 508  # LOOP_DETECTED: 检测到循环
    HTTP_509 = 509  # UNASSIGNED: 未分配
    HTTP_510 = 510  # NOT_EXTENDED: 未扩展
    HTTP_511 = 511  # NETWORK_AUTHENTICATION_REQUIRED: 需要网络身份验证

    """
    WebSocket codes
    https://www.iana.org/assignments/websocket/websocket.xml#close-code-number
    https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent
    """
    WS_1000 = 1000  # NORMAL_CLOSURE: 正常闭合
    WS_1001 = 1001  # GOING_AWAY: 正在离开
    WS_1002 = 1002  # PROTOCOL_ERROR: 协议错误
    WS_1003 = 1003  # UNSUPPORTED_DATA: 不支持的数据类型
    WS_1005 = 1005  # NO_STATUS_RCVD: 没有接收到状态
    WS_1006 = 1006  # ABNORMAL_CLOSURE: 异常关闭
    WS_1007 = 1007  # INVALID_FRAME_PAYLOAD_DATA: 无效的帧负载数据
    WS_1008 = 1008  # POLICY_VIOLATION: 策略违规
    WS_1009 = 1009  # MESSAGE_TOO_BIG: 消息太大
    WS_1010 = 1010  # MANDATORY_EXT: 必需的扩展
    WS_1011 = 1011  # INTERNAL_ERROR: 内部错误
    WS_1012 = 1012  # SERVICE_RESTART: 服务重启
    WS_1013 = 1013  # TRY_AGAIN_LATER: 请稍后重试
    WS_1014 = 1014  # BAD_GATEWAY: 错误的网关
    WS_1015 = 1015  # TLS_HANDSHAKE: TLS握手错误
    WS_3000 = 3000  # UNAUTHORIZED: 未经授权
    WS_3003 = 3003  # FORBIDDEN: 禁止访问
