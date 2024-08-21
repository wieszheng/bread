# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 12:54
@Author   : wiesZheng
@Software : PyCharm
"""
import time
import uuid

from fastapi import FastAPI, Request, Response
from loguru import logger


def add_custom_middleware(app: FastAPI):
    # 日志中间件 记录请求参数信息、计算响应时间
    @app.middleware("http")
    async def request_log_middleware(request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        request.state.traceid = uuid.uuid4()
        # 打印请求信息
        logger.info(
            f"--> {request.state.traceid} {request.method} {request.url.path} {request.client.host}"
        )
        if request.query_params:
            logger.info(
                f"--> {request.state.traceid} Query Params: {request.query_params}"
            )

        if "application/json" in request.headers.get("Content-Type", ""):
            # await set_body(request)
            try:
                # starlette 中间件中不能读取请求数据，否则会进入循环等待 需要特殊处理或者换APIRoute实现
                body = await request.json()
                logger.info(f"--> {request.state.traceid} Body: {body}")
            except Exception as e:
                logger.warning(f"Failed to parse JSON body: {e}")

        # 执行请求获取响应
        response = await call_next(request)

        # 计算响应时间
        process_time = time.perf_counter() - start_time
        response.headers["X-Response-Time"] = f"{process_time:.6f}s"
        logger.info(
            f"<-- {request.state.traceid} {response.status_code} {request.url.path} (took: {process_time:.6f}s)\n"
        )

        return response


async def set_body(request: Request):
    receive_ = await request.receive()

    async def receive():
        return receive_

    request._receive = receive
