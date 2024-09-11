# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2024/8/9 15:07
@Author   : wiesZheng
@Software : PyCharm
"""

from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, Optional, Union

from loguru import logger
from pydantic import BaseModel, ValidationError
from sqlalchemy import Join, Result, Row, Select, asc
from sqlalchemy import column as c
from sqlalchemy import delete, desc, func, inspect, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement

from app.commons import SingletonMetaCls
from app.crud.helper import (
    JoinConfig,
    _extract_matching_columns_from_schema,
    _get_primary_keys,
    _handle_null_primary_key_multi_join,
    _nest_join_data,
    _nest_multi_join_data,
)
from app.crud.types import CreateSchemaType, ModelType, UpdateSchemaType
from app.exceptions.errors import DBError
from app.models import async_session_maker


def with_session(method):
    """
    兼容事务
    Args:
        method: orm 的 crud
    Notes:
        方法中没有带事务连接则，则构造
    Returns:
    """

    @wraps(method)
    async def wrapper(cls, *args, **kwargs):
        try:
            session = kwargs.get("session") or None
            if session:
                return await method(cls, *args, **kwargs)
            else:
                async with async_session_maker() as session:
                    async with session.begin():
                        kwargs["session"] = session
                        return await method(cls, *args, **kwargs)
        except Exception as e:
            logger.error(
                f"操作Model：{cls.__model__.__name__}\n"
                f"方法：{method.__name__}\n"
                f"参数：args：{[*args]}, kwargs：{kwargs}\n"
                f"错误：{e}\n"
            )
            # logger.error(traceback.format_exc())
            raise DBError(f"操作数据库异常：{method.__name__}: {e}")

    return wrapper


class BaseCRUD(SingletonMetaCls):
    __model__: type[ModelType]
    is_deleted_column: str = "is_deleted"
    deleted_at_column: str = "deleted_at"
    updated_at_column: str = "updated_at"

    _SUPPORTED_FILTERS = {
        "gt": lambda column: column.__gt__,
        "lt": lambda column: column.__lt__,
        "gte": lambda column: column.__ge__,
        "lte": lambda column: column.__le__,
        "ne": lambda column: column.__ne__,
        "is": lambda column: column.is_,
        "is_not": lambda column: column.is_not,
        "like": lambda column: column.like,
        "notlike": lambda column: column.notlike,
        "ilike": lambda column: column.ilike,
        "notilike": lambda column: column.notilike,
        "startswith": lambda column: column.startswith,
        "endswith": lambda column: column.endswith,
        "contains": lambda column: column.contains,
        "match": lambda column: column.match,
        "between": lambda column: column.between,
        "in": lambda column: column.in_,
        "not_in": lambda column: column.not_in,
    }

    @classmethod
    def _get_sqlalchemy_filter(
        cls,
        operator: str,
        value: Any,
    ) -> Optional[Callable[[str], Callable]]:
        if operator in {"in", "not_in", "between"}:
            if not isinstance(value, (tuple, list, set)):
                raise ValueError(f"<{operator}> filter must be tuple, list or set")
        return cls._SUPPORTED_FILTERS.get(operator)

    @classmethod
    def _parse_filters(
        cls, model: Optional[Union[type[ModelType], AliasedClass]] = None, **kwargs
    ) -> list[ColumnElement]:
        model = model or cls.__model__
        filters = []

        for key, value in kwargs.items():
            if "__" in key:
                field_name, op = key.rsplit("__", 1)
                column_ = getattr(model, field_name, None)
                if column_ is None:
                    raise ValueError(f"Invalid filter column_: {field_name}")
                if op == "or":
                    or_filters = [
                        sqlalchemy_filter(column_)(or_value)
                        for or_key, or_value in value.items()
                        if (
                            sqlalchemy_filter := cls._get_sqlalchemy_filter(
                                or_key, value
                            )
                        )
                        is not None
                    ]
                    filters.append(or_(*or_filters))
                else:
                    sqlalchemy_filter = cls._get_sqlalchemy_filter(op, value)
                    if sqlalchemy_filter:
                        filters.append(sqlalchemy_filter(column_)(value))
            else:
                column_ = getattr(model, key, None)
                if column_ is not None:
                    if value is not None:
                        filters.append(column_ == value)

        return filters

    @classmethod
    def _apply_sorting(
        cls,
        stmt: Select,
        sort_columns: Union[str, list[str]],
        sort_orders: Optional[Union[str, list[str]]] = None,
    ) -> Select:
        if sort_orders and not sort_columns:
            raise ValueError("Sort orders provided without corresponding sort columns.")

        if sort_columns:
            if not isinstance(sort_columns, list):
                sort_columns = [sort_columns]

            if sort_orders:
                if not isinstance(sort_orders, list):
                    sort_orders = [sort_orders] * len(sort_columns)
                if len(sort_columns) != len(sort_orders):
                    raise ValueError(
                        "The length of sort_columns and sort_orders must match."
                    )

                for idx, order in enumerate(sort_orders):
                    if order not in ["asc", "desc"]:
                        raise ValueError(
                            f"Invalid sort order: {order}. Only 'asc' or 'desc' are allowed."
                        )

            validated_sort_orders = (
                ["asc"] * len(sort_columns) if not sort_orders else sort_orders
            )

            for idx, column_name in enumerate(sort_columns):
                column = getattr(cls.__model__, column_name, None)
                if not column:
                    raise ValueError(f"Invalid column name: {column_name}")

                order = validated_sort_orders[idx]
                stmt = stmt.order_by(asc(column) if order == "asc" else desc(column))

        return stmt

    @classmethod
    def _prepare_and_apply_joins(
        cls,
        stmt: Select,
        joins_config: list[JoinConfig],
        use_temporary_prefix: bool = False,
    ):
        for join in joins_config:
            model = join.alias or join.model
            join_select = _extract_matching_columns_from_schema(
                model,
                join.schema_to_select,
                join.join_prefix,
                join.alias,
                use_temporary_prefix,
            )
            joined_model_filters = cls._parse_filters(
                model=model, **(join.filters or {})
            )

            if join.join_type == "left":
                stmt = stmt.outerjoin(model, join.join_on).add_columns(*join_select)
            elif join.join_type == "inner":
                stmt = stmt.join(model, join.join_on).add_columns(*join_select)
            else:  # pragma: no cover
                raise ValueError(f"Unsupported join type: {join.join_type}.")
            if joined_model_filters:
                stmt = stmt.filter(*joined_model_filters)

        return stmt

    @classmethod
    @with_session
    async def _insert(
        cls,
        *,
        case_id: int,
        user_id: int,
        form: Optional[type[BaseModel]],
        commit: bool = True,
        session: AsyncSession = None,
        **fields: tuple,
    ):
        for field, model_info in fields.items():
            md, model = model_info
            field_data = getattr(form, field)
            for f in field_data:
                if hasattr(f, "case_id"):
                    setattr(f, "case_id", case_id)
                    object_mt: ModelType = model(**f.model_dump(), user_id=user_id)
                else:
                    object_mt: ModelType = model(
                        **f.model_dump(), user_id=user_id, case_id=case_id
                    )

                session.add(object_mt)
                if commit:
                    await session.commit()

    @classmethod
    @with_session
    async def create(
        cls,
        *,
        obj: CreateSchemaType,
        commit: bool = True,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> ModelType:
        object_dict = obj.model_dump()
        object_mt: ModelType = cls.__model__(**object_dict, **kwargs)
        session.add(object_mt)
        if commit:
            await session.commit()
        return object_mt

    @classmethod
    async def select(
        cls,
        *,
        schema_to_select: Optional[type[BaseModel]] = None,
        sort_columns: Optional[Union[str, list[str]]] = None,
        sort_orders: Optional[Union[str, list[str]]] = None,
        **kwargs: Any,
    ) -> Select:
        to_select = _extract_matching_columns_from_schema(
            model=cls.__model__, schema=schema_to_select
        )
        filters = cls._parse_filters(**kwargs)
        stmt = select(*to_select).filter(*filters)

        if sort_columns:
            stmt = cls._apply_sorting(stmt, sort_columns, sort_orders)
        return stmt

    @classmethod
    @with_session
    async def get(
        cls,
        *,
        schema_to_select: Optional[type[BaseModel]] = None,
        return_as_model: bool = False,
        one_or_none: bool = False,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> Optional[Union[dict, BaseModel]]:
        stmt = await cls.select(schema_to_select=schema_to_select, **kwargs)

        db_row = await session.execute(stmt)
        result: Optional[Row] = db_row.one_or_none() if one_or_none else db_row.first()
        if result is None:
            return None
        out: dict = dict(result._mapping)
        if not return_as_model:
            return out
        if not schema_to_select:
            raise ValueError(
                "schema_to_select must be provided when return_as_model is True."
            )
        return schema_to_select(**out)

    @classmethod
    @with_session
    async def get_all(
        cls,
        *,
        schema_to_select: Optional[type[BaseModel]] = None,
        return_as_model: bool = False,
        return_total_count: bool = True,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> Optional[Union[dict, BaseModel]]:
        stmt = await cls.select(schema_to_select=schema_to_select, **kwargs)
        result = await session.execute(stmt)
        data = [dict(row) for row in result.mappings()]
        response: dict[str, Any] = {"data": data}
        if return_total_count:
            total_count = await cls.count(**kwargs)
            response["total_count"] = total_count

        if return_as_model:
            if not schema_to_select:
                raise ValueError(
                    "schema_to_select must be provided when return_as_model is True."
                )
            try:
                model_data = [schema_to_select(**row) for row in data]
                response["data"] = model_data
            except ValidationError as e:
                raise ValueError(
                    f"Data validation error for schema {schema_to_select.__name__}: {e}"
                )
        return response

    @classmethod
    def _get_pk_dict(cls, instance):
        return {
            pk.name: getattr(instance, pk.name)
            for pk in _get_primary_keys(cls.__model__)
        }

    @classmethod
    async def upsert(
        cls,
        *,
        instance: Union[UpdateSchemaType, CreateSchemaType],
        schema_to_select: Optional[type[BaseModel]] = None,
        return_as_model: bool = False,
    ) -> Union[BaseModel, Dict[str, Any], None]:
        _pks = cls._get_pk_dict(instance)
        schema_to_select = schema_to_select or type(instance)
        db_instance = await cls.get(
            schema_to_select=schema_to_select,
            return_as_model=return_as_model,
            **_pks,
        )
        if db_instance is None:
            db_instance = await cls.create(instance)  # type: ignore
            db_instance = schema_to_select.model_validate(
                db_instance, from_attributes=True
            )
        else:
            await cls.update(instance)  # type: ignore
            db_instance = await cls.get(
                schema_to_select=schema_to_select,
                return_as_model=return_as_model,
                **_pks,
            )

        return db_instance

    @classmethod
    @with_session
    async def exists(cls, session: AsyncSession = None, **kwargs: Any) -> bool:
        filters = cls._parse_filters(**kwargs)
        stmt = select(cls.__model__).filter(*filters).limit(1)

        result = await session.execute(stmt)
        return result.first() is not None

    @classmethod
    @with_session
    async def count(
        cls,
        *,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> int:
        filters = cls._parse_filters(**kwargs)
        if filters:
            count_query = (
                select(func.count()).select_from(cls.__model__).filter(*filters)
            )
        else:
            count_query = select(func.count()).select_from(cls.__model__)

        total_count = await session.scalar(count_query)
        return total_count

    @classmethod
    @with_session
    async def get_multi(
        cls,
        *,
        offset: int = 0,
        limit: Optional[int] = 100,
        schema_to_select: Optional[type[BaseModel]] = None,
        sort_columns: Optional[Union[str, list[str]]] = None,
        sort_orders: Optional[Union[str, list[str]]] = None,
        return_as_model: bool = False,
        return_total_count: bool = True,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if (limit is not None and limit < 0) or offset < 0:
            raise ValueError("Limit and offset must be non-negative.")

        stmt = await cls.select(
            schema_to_select=schema_to_select,
            sort_columns=sort_columns,
            sort_orders=sort_orders,
            **kwargs,
        )

        if offset:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await session.execute(stmt)
        data = [dict(row) for row in result.mappings()]

        response: dict[str, Any] = {"data": data}

        if return_total_count:
            total_count = await cls.count(**kwargs)
            response["total_count"] = total_count

        if return_as_model:
            if not schema_to_select:
                raise ValueError(
                    "schema_to_select must be provided when return_as_model is True."
                )
            try:
                model_data = [schema_to_select(**row) for row in data]
                response["data"] = model_data
            except ValidationError as e:
                raise ValueError(
                    f"Data validation error for schema {schema_to_select.__name__}: {e}"
                )

        return response

    @classmethod
    @with_session
    async def get_joined(
        cls,
        *,
        schema_to_select: Optional[type[BaseModel]] = None,
        join_model: Optional[ModelType] = None,
        join_on: Optional[Union[Join, BinaryExpression]] = None,
        join_prefix: Optional[str] = None,
        join_schema_to_select: Optional[type[BaseModel]] = None,
        join_type: str = "left",
        alias: Optional[AliasedClass] = None,
        join_filters: Optional[dict] = None,
        joins_config: Optional[list[JoinConfig]] = None,
        nest_joins: bool = False,
        relationship_type: Optional[str] = None,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> Optional[dict[str, Any]]:
        if joins_config and (
            join_model or join_prefix or join_on or join_schema_to_select or alias
        ):
            raise ValueError(
                "Cannot use both single join parameters and joins_config simultaneously."
            )
        elif not joins_config and not join_model:
            raise ValueError("You need one of join_model or joins_config.")

        primary_select = _extract_matching_columns_from_schema(
            model=cls.__model__,
            schema=schema_to_select,
        )
        stmt: Select = select(*primary_select).select_from(cls.__model__)

        join_definitions = joins_config if joins_config else []
        if join_model:
            join_definitions.append(
                JoinConfig(
                    model=join_model,
                    join_on=join_on,
                    join_prefix=join_prefix,
                    schema_to_select=join_schema_to_select,
                    join_type=join_type,
                    alias=alias,
                    filters=join_filters,
                    relationship_type=relationship_type,
                )
            )

        stmt = cls._prepare_and_apply_joins(
            stmt=stmt, joins_config=join_definitions, use_temporary_prefix=nest_joins
        )
        primary_filters = cls._parse_filters(**kwargs)
        if primary_filters:
            stmt = stmt.filter(*primary_filters)

        db_rows = await session.execute(stmt)
        if any(join.relationship_type == "one-to-many" for join in join_definitions):
            if nest_joins is False:  # pragma: no cover
                raise ValueError(
                    "Cannot use one-to-many relationship with nest_joins=False"
                )
            results = db_rows.fetchall()
            data_list = [dict(row._mapping) for row in results]
        else:
            result = db_rows.first()
            if result is not None:
                data_list = [dict(result._mapping)]
            else:
                data_list = []

        if data_list:
            if nest_joins:
                nested_data: dict = {}
                for data in data_list:
                    nested_data = _nest_join_data(
                        data,
                        join_definitions,
                        nested_data=nested_data,
                    )
                return nested_data
            return data_list[0]

        return None

    @classmethod
    @with_session
    async def get_multi_joined(
        cls,
        *,
        schema_to_select: Optional[type[BaseModel]] = None,
        join_model: Optional[type[ModelType]] = None,
        join_on: Optional[Any] = None,
        join_prefix: Optional[str] = None,
        join_schema_to_select: Optional[type[BaseModel]] = None,
        join_type: str = "left",
        alias: Optional[AliasedClass[Any]] = None,
        join_filters: Optional[dict] = None,
        nest_joins: bool = False,
        offset: int = 0,
        limit: Optional[int] = 100,
        sort_columns: Optional[Union[str, list[str]]] = None,
        sort_orders: Optional[Union[str, list[str]]] = None,
        return_as_model: bool = False,
        joins_config: Optional[list[JoinConfig]] = None,
        return_total_count: bool = True,
        relationship_type: Optional[str] = None,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        users = await user_crud.get_multi_joined(
            db=session,
            schema_to_select=ReadUserSchema,
            joins_config=[
                JoinConfig(
                    model=Tier,
                    join_on=User.tier_id == Tier.id,
                    join_prefix="tier_",
                    schema_to_select=ReadTierSchema,
                    join_type="left",
                ),
                JoinConfig(
                    model=Department,
                    join_on=User.department_id == Department.id,
                    join_prefix="dept_",
                    schema_to_select=ReadDepartmentSchema,
                    join_type="inner",
                ),
            ],
            offset=0,
            limit=10,
            sort_columns='username',
            sort_orders='asc',
        )

        stories = await story_crud.get_multi_joined(
            db=session,
            schema_to_select=ReadStorySchema,
            joins_config=[
                JoinConfig(
                    model=Task,
                    join_on=Story.id == Task.story_id,
                    join_prefix="task_",
                    schema_to_select=ReadTaskSchema,
                    join_type="left",
                ),
                JoinConfig(
                    model=User,
                    join_on=Task.creator_id == User.id,
                    join_prefix="creator_",
                    schema_to_select=ReadUserSchema,
                    join_type="left",
                    alias=aliased(User, name="task_creator"),
                ),
            ],
            nest_joins=True,
            offset=0,
            limit=5,
            sort_columns='name',
            sort_orders='asc',
        )
        """
        if joins_config and (
            join_model
            or join_prefix
            or join_on
            or join_schema_to_select
            or alias
            or relationship_type
        ):
            raise ValueError(
                "Cannot use both single join parameters and joins_config simultaneously."
            )
        elif not joins_config and not join_model:
            raise ValueError("You need one of join_model or joins_config.")

        if (limit is not None and limit < 0) or offset < 0:
            raise ValueError("Limit and offset must be non-negative.")

        if relationship_type is None:
            relationship_type = "one-to-one"

        primary_select = _extract_matching_columns_from_schema(
            model=cls.__model__, schema=schema_to_select
        )
        stmt: Select = select(*primary_select)

        join_definitions = joins_config if joins_config else []

        if join_model:
            join_definitions.append(
                JoinConfig(
                    model=join_model,
                    join_on=join_on,
                    join_prefix=join_prefix,
                    schema_to_select=join_schema_to_select,
                    join_type=join_type,
                    alias=alias,
                    filters=join_filters,
                    relationship_type=relationship_type,
                )
            )

        stmt = cls._prepare_and_apply_joins(
            stmt=stmt, joins_config=join_definitions, use_temporary_prefix=nest_joins
        )

        primary_filters = cls._parse_filters(**kwargs)
        if primary_filters:
            stmt = stmt.filter(*primary_filters)

        if sort_columns:
            stmt = cls._apply_sorting(stmt, sort_columns, sort_orders)

        if offset:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await session.execute(stmt)
        data: list[Union[dict, BaseModel]] = []

        for row in result.mappings().all():
            row_dict = dict(row)

            if nest_joins:
                row_dict = _nest_join_data(
                    data=row_dict,
                    join_definitions=join_definitions,
                )

            if return_as_model:
                if schema_to_select is None:
                    raise ValueError(
                        "schema_to_select must be provided when return_as_model is True."
                    )
                try:
                    model_instance = schema_to_select(**row_dict)
                    data.append(model_instance)
                except ValidationError as e:
                    raise ValueError(
                        f"Data validation error for schema {schema_to_select.__name__}: {e}"
                    )
            else:
                data.append(row_dict)

        if nest_joins and any(
            join.relationship_type == "one-to-many" for join in join_definitions
        ):
            nested_data = _nest_multi_join_data(
                base_primary_key=_get_primary_keys(cls.__model__)[0].name,
                data=data,
                joins_config=join_definitions,
                return_as_model=return_as_model,
                schema_to_select=schema_to_select if return_as_model else None,
                nested_schema_to_select={
                    (
                        join.join_prefix.rstrip("_")
                        if join.join_prefix
                        else join.model.__name__
                    ): join.schema_to_select
                    for join in join_definitions
                    if join.schema_to_select
                },
            )
        else:
            nested_data = _handle_null_primary_key_multi_join(data, join_definitions)

        response: dict[str, Any] = {"data": nested_data}

        if return_total_count:
            total_count: int = await cls.count(
                db=session, joins_config=joins_config, **kwargs
            )
            response["total_count"] = total_count

        return response

    @classmethod
    @with_session
    async def get_multi_by_cursor(
        cls,
        *,
        cursor: Any = None,
        limit: int = 100,
        schema_to_select: Optional[type[BaseModel]] = None,
        sort_column: str = "id",
        sort_order: str = "asc",
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if limit == 0:
            return {"data": [], "next_cursor": None}

        stmt = await cls.select(
            schema_to_select=schema_to_select,
            **kwargs,
        )

        if cursor:
            if sort_order == "asc":
                stmt = stmt.filter(getattr(cls.__model__, sort_column) > cursor)
            else:
                stmt = stmt.filter(getattr(cls.__model__, sort_column) < cursor)

        stmt = stmt.order_by(
            asc(getattr(cls.__model__, sort_column))
            if sort_order == "asc"
            else desc(getattr(cls.__model__, sort_column))
        )
        stmt = stmt.limit(limit)

        result = await session.execute(stmt)
        data = [dict(row) for row in result.mappings()]

        next_cursor = None
        if len(data) == limit:
            if sort_order == "asc":
                next_cursor = data[-1][sort_column]
            else:
                data[0][sort_column]

        return {"data": data, "next_cursor": next_cursor}

    @classmethod
    def _as_single_response(
        cls,
        db_row: Result,
        schema_to_select: Optional[type[BaseModel]] = None,
        return_as_model: bool = False,
        one_or_none: bool = False,
    ) -> Optional[Union[dict, BaseModel]]:
        result: Optional[Row] = db_row.one_or_none() if one_or_none else db_row.first()
        if result is None:  # pragma: no cover
            return None
        out: dict = dict(result._mapping)
        if not return_as_model:
            return out
        if not schema_to_select:  # pragma: no cover
            raise ValueError(
                "schema_to_select must be provided when return_as_model is True."
            )
        return schema_to_select(**out)

    @classmethod
    def _as_multi_response(
        cls,
        db_row: Result,
        schema_to_select: Optional[type[BaseModel]] = None,
        return_as_model: bool = False,
    ) -> dict:
        data = [dict(row) for row in db_row.mappings()]

        response: dict[str, Any] = {"data": data}

        if return_as_model:
            if not schema_to_select:  # pragma: no cover
                raise ValueError(
                    "schema_to_select must be provided when return_as_model is True."
                )
            try:
                model_data = [schema_to_select(**row) for row in data]
                response["data"] = model_data
            except ValidationError as e:  # pragma: no cover
                raise ValueError(
                    f"Data validation error for schema {schema_to_select.__name__}: {e}"
                )

        return response

    @classmethod
    @with_session
    async def update(
        cls,
        *,
        obj: Union[UpdateSchemaType, dict[str, Any]],
        allow_multiple: bool = False,
        commit: bool = True,
        return_columns: Optional[list[str]] = None,
        schema_to_select: Optional[type[BaseModel]] = None,
        return_as_model: bool = False,
        one_or_none: bool = False,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> Optional[Union[dict, BaseModel]]:
        if not allow_multiple and (total_count := await cls.count(**kwargs)) > 1:
            raise ValueError(
                f"Expected exactly one record to update, found {total_count}."
            )
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.model_dump(exclude_unset=True)

        updated_at_col = getattr(cls.__model__, cls.updated_at_column, None)
        if updated_at_col:
            update_data[cls.updated_at_column] = datetime.now()

        update_data_keys = set(update_data.keys())
        model_columns = {column_.name for column_ in inspect(cls.__model__).c}
        extra_fields = update_data_keys - model_columns
        if extra_fields:
            raise ValueError(f"Extra fields provided: {extra_fields}")

        filters = cls._parse_filters(**kwargs)
        stmt = update(cls.__model__).filter(*filters).values(update_data)

        if return_as_model:
            return_columns = [col.key for col in cls.__model__.__table__.columns]

        if return_columns:
            stmt = stmt.returning(*[c(name) for name in return_columns])
            db_row = await session.execute(stmt)
            if allow_multiple:
                return cls._as_multi_response(
                    db_row,
                    schema_to_select=schema_to_select,
                    return_as_model=return_as_model,
                )
            return cls._as_single_response(
                db_row,
                schema_to_select=schema_to_select,
                return_as_model=return_as_model,
                one_or_none=one_or_none,
            )

        await session.execute(stmt)
        if commit:
            await session.commit()
        return None

    @classmethod
    @with_session
    async def db_delete(
        cls,
        allow_multiple: bool = False,
        commit: bool = True,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> None:
        if not allow_multiple and (total_count := await cls.count(**kwargs)) > 1:
            raise ValueError(
                f"Expected exactly one record to delete, found {total_count}."
            )

        filters = cls._parse_filters(**kwargs)
        stmt = delete(cls.__model__).filter(*filters)
        await session.execute(stmt)
        if commit:
            await session.commit()

    @classmethod
    @with_session
    async def delete(
        cls,
        db_row: Optional[Row] = None,
        allow_multiple: bool = False,
        commit: bool = True,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> None:
        filters = cls._parse_filters(**kwargs)
        if db_row:
            if hasattr(db_row, cls.is_deleted_column) and hasattr(
                db_row, cls.deleted_at_column
            ):
                setattr(db_row, cls.is_deleted_column, True)
                setattr(db_row, cls.deleted_at_column, datetime.now())
                if commit:
                    await session.commit()
            else:
                await session.delete(db_row)
            if commit:
                await session.commit()
            return

        total_count = await cls.count(**kwargs)
        if total_count == 0:
            raise ValueError("No record found to delete.")
        if not allow_multiple and total_count > 1:
            raise ValueError(
                f"Expected exactly one record to delete, found {total_count}."
            )
        logger.debug([col.key for col in cls.__model__.__table__.columns])
        if cls.is_deleted_column in [
            col.key for col in cls.__model__.__table__.columns
        ]:
            update_stmt = (
                update(cls.__model__)
                .filter(*filters)
                .values(is_deleted=True, deleted_at=datetime.now())
            )
            logger.debug(update_stmt)
            await session.execute(update_stmt)
        else:
            delete_stmt = delete(cls.__model__).filter(*filters)
            await session.execute(delete_stmt)

        if commit:
            await session.commit()
