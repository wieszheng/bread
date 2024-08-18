#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 0:12
@Author   : wiesZheng
@Software : PyCharm
"""
import argparse
import os
import sys
import time
from functools import lru_cache
from typing import ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

ROOT = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(ROOT, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# 项目运行时所有的日志文件
SERVER_LOG_FILE: str = os.path.join(LOG_DIR, f'{time.strftime("%Y-%m-%d")}_server.log')

# 错误时的日志文件
ERROR_LOG_FILE: str = os.path.join(LOG_DIR, f'{time.strftime("%Y-%m-%d")}_error.log')


class AppSettings(BaseSettings):
    """
    应用配置
    """

    APP_ENV: str
    APP_NAME: str
    APP_ROOT_PATH: str
    APP_HOST: str
    APP_PORT: int
    APP_VERSION: str
    APP_RELOAD: bool
    APP_IP_LOCATION_QUERY: bool
    APP_SAME_TIME_LOGIN: bool

    # 权限 0 普通用户 1 组长 2 管理员
    MEMBER: int
    MANAGER: int
    ADMIN: int

    # 密码加密配置
    BCRYPT_ROUNDS: int  # bcrypt迭代次数,越大耗时越长
    SALT: str

    # 项目日志滚动配置（日志文件超过10 MB就自动新建文件扩充）
    LOGGING_ROTATION: str = "10 MB"
    LOGGING_CONF: dict = {
        "server_handler": {
            "file": SERVER_LOG_FILE,
            "level": "INFO",
            "rotation": LOGGING_ROTATION,
            "backtrace": False,
            "diagnose": False,
        },
        "error_handler": {
            "file": ERROR_LOG_FILE,
            "level": "ERROR",
            "rotation": LOGGING_ROTATION,
            "backtrace": True,
            "diagnose": True,
        },
    }

    BANNER: str = """
                                      \`-,                             
                                      |   `\                           
                                      |     \                          
                                   __/.- - -.\,__                      
                              _.-'`              `'"'--..,__           
                          .-'`                              `'--.,_    
                       .'`   _                         _ ___       `)  
                     .'   .'` `'-.                    (_`  _`)  _.-'   
                   .'    '--.     '.                 .-.`"`@ .-'""-,   
          .------~'     ,.---'      '-._      _.'   /   `'--':::.-'   
        /`        '   /`  _,..-----.,__ `''''`/    ;__,..--''--'`      
        `'--.,__ '    |-'`             `'---'|     |                   
                `\    \                       \   /                    
                 |     |                       '-'                     
                  \    |                                               
                   `\  |                                               
                     \/  

            """


class JwtSettings(BaseSettings):
    """
    Jwt配置
    """

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int
    JWT_REDIS_EXPIRE_MINUTES: int
    JWT_ISS: str


class DataBaseSettings(BaseSettings):
    """
    数据库配置
    """

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_PROTOCOL: str
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_ECHO: bool
    MYSQL_MAX_OVERFLOW: int
    MYSQL_POOL_SIZE: int
    MYSQL_POOL_RECYCLE: int
    MYSQL_POOL_TIMEOUT: int


class RedisSettings(BaseSettings):
    """
    Redis配置
    """

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    REDIS_DATABASE: int


class MinioSettings(BaseSettings):
    """
    Minio配置
    """

    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool
    MINIO_BUCKET_NAME: str
    MINIO_BUCKET_ACCESS_KEY: str
    MINIO_BUCKET_SECRET_KEY: str


class GetConfig:
    """
    获取配置
    """

    def __init__(self):
        self.parse_cli_args()

    @lru_cache()
    def get_app_config(self):
        """
        获取应用配置
        """
        # 实例化应用配置模型
        return AppSettings()

    @lru_cache()
    def get_jwt_config(self):
        """
        获取Jwt配置
        """
        # 实例化Jwt配置模型
        return JwtSettings()

    @lru_cache()
    def get_database_config(self):
        """
        获取数据库配置
        """
        # 实例化数据库配置模型
        return DataBaseSettings()

    @lru_cache()
    def get_redis_config(self):
        """
        获取Redis配置
        """
        # 实例化Redis配置模型
        return RedisSettings()

    @lru_cache()
    def get_minio_config(self):
        """
        获取Minio配置
        """
        # 实例化Minio配置模型
        return MinioSettings()

    @staticmethod
    def parse_cli_args():
        """
        解析命令行参数
        """
        if "uvicorn" in sys.argv[0]:
            pass
        else:
            parser = argparse.ArgumentParser(description="命令行参数")
            parser.add_argument("--env", type=str, default="", help="运行环境")

            args, unknown = parser.parse_known_args()
            os.environ["APP_ENV"] = args.env if args.env else "dev"

        run_env = os.environ.get("APP_ENV", "")
        env_file = ".env.dev"
        if run_env != "":
            env_file = f".env.{run_env}"
        # 加载配置
        load_dotenv(os.path.join(ROOT, "conf", env_file))


# 实例化获取配置类
get_config = GetConfig()

# 应用配置
AppConfig = get_config.get_app_config()
# Jwt配置
JwtConfig = get_config.get_jwt_config()
# 数据库配置
DataBaseConfig = get_config.get_database_config()
# Redis配置
RedisConfig = get_config.get_redis_config()
# Minio配置
MinioConfig = get_config.get_minio_config()

# def get_all_configs():
#     # 实例化获取配置类
#     get_config = GetConfig()
#
#     # 定义配置名称及其对应的获取方法
#     config_methods = {
#         'app': get_config.get_app_config,
#         'jwt': get_config.get_jwt_config,
#         'database': get_config.get_database_config,
#         'redis': get_config.get_redis_config,
#         'minio': get_config.get_minio_config,
#     }
#
#     # 创建一个字典来存储配置
#     configs = {}
#
#     # 遍历字典获取配置
#     for name, method in config_methods.items():
#         configs[name] = method()
#
#     return configs
#
#
# # 调用函数获取所有配置
# conf = get_all_configs()
