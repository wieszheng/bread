# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/7 17:16
@Author   : wiesZheng
@Software : PyCharm
"""
import os

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from starlette.staticfiles import StaticFiles

from app import init_logging, lifespan
from app.commons.openapi import get_stoplight_ui_html
from app.exceptions import register_exceptions_handler
from app.middlewares import register_middlewares
from config import ROOT, settings

app = FastAPI(
    title=settings.APP_NAME,
    description=f'{settings.APP_NAME} 接口文档',
    version=settings.APP_VERSION,
    # root_path=AppConfig.APP_ROOT_PATH,
    lifespan=lifespan,
)
# 挂载静态文件目录
app.mount('/static', StaticFiles(directory=f'{ROOT}/static'), name='static')


# stoplight_elements doc
@app.get("/openapi", include_in_schema=False)
async def api_documentation():
    """Add stoplight elements api doc. https://dev.to/amal/replacing-fastapis-default-api-docs-with-elements-391d"""
    return get_stoplight_ui_html(
        openapi_url='/openapi.json',
        title=settings.APP_NAME + " - openapi",
        # base_path="openapi",
        logo='/static/Baguette Bread.png',
        stoplight_elements_favicon_url='/static/Baguette Bread.png',
    )


@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title=settings.APP_NAME + ' - Swagger UI',
        swagger_js_url='/static/swagger_ui/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger_ui/swagger-ui.css',
        swagger_favicon_url='/static/favicon.ico',
    )


@app.get('/redoc', include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url='/openapi.json',
        title=settings.APP_NAME + ' - ReDoc',
        redoc_js_url='/static/redoc_ui/redoc.standalone.js',
        redoc_favicon_url='/static/favicon.ico',
    )


# 初始化日志
init_logging(settings.LOGGING_CONF)
# 注册中间件处理方法
register_middlewares(app)
# 注册全局异常处理方法
register_exceptions_handler(app)
