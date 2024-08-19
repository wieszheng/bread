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
from app.exceptions import register_exceptions_handler
from app.middlewares import register_middlewares
from config import AppConfig, ROOT
from starlette.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

app = FastAPI(
    title=AppConfig.APP_NAME,
    description=f"{AppConfig.APP_NAME} 接口文档",
    version=AppConfig.APP_VERSION,
    # root_path=AppConfig.APP_ROOT_PATH,
    lifespan=lifespan,
)
# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=f"{ROOT}/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=AppConfig.APP_NAME + " - Swagger UI",
        swagger_js_url="/static/swagger_ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger_ui/swagger-ui.css",
        swagger_favicon_url="/static/favicon.ico",
    )


@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=AppConfig.APP_NAME + " - ReDoc",
        redoc_js_url="/static/redoc_ui/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.ico",
    )


# 初始化日志
init_logging(AppConfig.LOGGING_CONF)
# 注册中间件处理方法
register_middlewares(app)
# 注册全局异常处理方法
register_exceptions_handler(app)
