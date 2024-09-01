# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/15 10:55
@Author   : wiesZheng
@Software : PyCharm
"""
max_length = max(
    len(line.split("=")[0].strip())
    for line in [
        "__table_args__",
        "id",
        "creation_date",
        "created_by",
        "updation_date",
        "updated_by",
    ]
)


# 定义一个函数来格式化每一行
def format_line(name, value, comment):
    padding = " " * (max_length - len(name) + 5)  # 增加4个空格作为额外的间隔
    return f"{name}{padding}={value}#{comment}\n"


# 格式化每一行
formatted_lines = [
    format_line("__table_args__", "{'mysql_charset': 'utf8'}", "设置表的字符集"),
    format_line(
        "id",
        "mapped_column(BigInteger(), nullable=False, primary_key=True, autoincrement=True)",
        "主键",
    ),
    format_line(
        "creation_date", "mapped_column(DateTime(), default=func.now())", "创建时间"
    ),
    format_line("created_by", "mapped_column(BigInteger)", "创建人ID"),
    format_line(
        "updation_date",
        "mapped_column(DateTime(), default=func.now(), onupdate=func.now())",
        "更新时间",
    ),
    format_line("updated_by", "mapped_column(BigInteger)", "更新人ID"),
]

# 输出格式化的结果
print("".join(formatted_lines))
name = None
if not name:
    filters = {"name__like": name}
    print(filters)
