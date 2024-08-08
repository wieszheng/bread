# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:16
@Author   : wiesZheng
@Software : PyCharm
"""
from fastapi import FastAPI

from app import lifespan, init_logging
from app.exceptions import register_global_exceptions_handler
from app.middlewares import register_middlewares
from config import AppConfig, ROOT
from starlette.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title=AppConfig.APP_NAME,
    description=f'{AppConfig.APP_NAME} 接口文档',
    version=AppConfig.APP_VERSION,
    root_path=AppConfig.APP_ROOT_PATH,
    lifespan=lifespan
)
app.mount("/static", StaticFiles(directory=f"{ROOT}/static"), name="static")


# @app.get('/docs', include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url="/openapi.json",
#         title=AppConfig.APP_NAME + " - Swagger UI",
#         swagger_js_url="/static/swagger-ui-bundle.js",
#         swagger_css_url="/static/swagger-ui.css"
#     )


# 初始化日志
init_logging(AppConfig.LOGGING_CONF)
# 注册中间件处理方法
register_middlewares(app)
# 注册全局异常处理方法
register_global_exceptions_handler(app)
