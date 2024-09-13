#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 0:12
@Author   : wiesZheng
@Software : PyCharm
"""

import os
import sys
import time
from argparse import ArgumentParser
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

ROOT = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(ROOT, 'logs')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# 项目运行时所有的日志文件
SERVER_LOG_FILE: str = os.path.join(LOG_DIR, f'{time.strftime('%Y-%m-%d')}_server.log')

# 错误时的日志文件
ERROR_LOG_FILE: str = os.path.join(LOG_DIR, f'{time.strftime('%Y-%m-%d')}_error.log')


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

    # 项目日志滚动配置（日志文件超过10 MB就自动新建文件扩充）
    LOGGING_ROTATION: str = '10 MB'
    LOGGING_CONF: dict = {
        'server_handler': {
            'file': SERVER_LOG_FILE,
            'level': 'INFO',
            'rotation': LOGGING_ROTATION,
            'backtrace': False,
            'diagnose': False,
        },
        'error_handler': {
            'file': ERROR_LOG_FILE,
            'level': 'ERROR',
            'rotation': LOGGING_ROTATION,
            'backtrace': True,
            'diagnose': True,
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


class CryptSettings(BaseSettings):
    # 密码加密配置
    BCRYPT_ROUNDS: int  # bcrypt迭代次数,越大耗时越长
    SALT: str


class JwtSettings(BaseSettings):
    """
    Jwt配置
    """

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int
    JWT_REDIS_EXPIRE_MINUTES: int
    JWT_ISS: str


class DatabaseSettings(BaseSettings):
    pass


class MySQLSettings(DatabaseSettings):
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


class RedisSettings(DatabaseSettings):
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


def get_env_file() -> str:
    """
    .env 文件路径
    """
    run_env = os.environ.get('APP_ENV', '')
    env_file = '.env.dev'
    if run_env != '':
        env_file = f'.env.{run_env}'
    return env_file


def parse_cli_args():
    """
    解析命令行参数
    """
    if 'uvicorn' in sys.argv[0]:
        pass
    else:
        parser = ArgumentParser(description='命令行参数')
        parser.add_argument('--env', type=str, default='', help='运行环境')

        args, _ = parser.parse_known_args()
        os.environ['APP_ENV'] = args.env if args.env else 'dev'

    # 加载配置
    load_dotenv(os.path.join(ROOT, 'conf', get_env_file()))


class Settings(
    AppSettings,
    CryptSettings,
    JwtSettings,
    MySQLSettings,
    RedisSettings,
    MinioSettings,
):
    pass


@lru_cache
def get_settings() -> Settings:
    """获取全局配置"""
    parse_cli_args()
    return Settings()


# 实例化获取配置类
settings = get_settings()
