# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 10:58
@Author   : wiesZheng
@Software : PyCharm
"""

from contextlib import asynccontextmanager

from art import text2art
from fastapi import FastAPI
from loguru import logger

from app.apis.v1 import register_routers
from app.models import Base, async_engine
from config import settings


def init_logging(logging_conf: dict):
    for log_handler, log_conf in logging_conf.items():
        log_file = log_conf.pop("file", None)
        logger.add(log_file, **log_conf)
    logger.info("setup logging success")


async def init_create_table():
    # 根据映射创建库表（异步）
    logger.info("初始化数据库连接...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("数据库连接成功")


# 生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    logger.info(f"{settings.APP_NAME} 开始启动")
    logger.success(text2art(settings.APP_NAME, font="block", chr_ignore=True))
    await init_create_table()
    await register_routers(app)
    logger.info(f"{settings.APP_NAME} 启动成功")
    yield
    # Clean up the ML models and release the resources
    logger.info(f"{settings.APP_NAME} 关闭成功")
