import operator
import sqlite3
from typing import AnyStr

import psycopg2

from uniorm import fields
from uniorm.conditions import Condition
from uniorm.schema import DataSchema

from .base import Backend, BackendException, BackendResultIterator

TYPE_MAPPING = {
    'string': 'varchar(255)',
    'integer': 'int',
}

SQL_OPERATOR_MAP = {
    operator.and_: "AND",
    operator.eq: "=",
    operator.not_: "NOT",
    operator.ne: "!=",
    operator.is_: "IS",
    operator.is_not: "IS NOT"
}

SUPPORTED_DRIVERS = {
    'sqlite3': sqlite3,
    'postgresql': psycopg2
}


TYPE_PARSERS = {
    int: lambda x: x,
    str: lambda x: f"'{x}'",
    type(None): lambda x: 'NULL'
}


class SQLBackendResultIterator(BackendResultIterator):
    def __next__(self):
        row = next(self.result)
        _dict = {i: j for i, j in zip(self.fields, row)}
        return self.schema_class(**_dict)


class SQLBackend(Backend):
    def __init__(self, connection=None) -> None:
        self.connection = connection

    @staticmethod
    def _get_driver(name):
        return SUPPORTED_DRIVERS[name]

    def _get_connection(self):
        if self.connection is None:
            raise BackendException('Connection is not created.')
        return self.connection

    def create_connection(self, driver, *args, **kwargs):
        driver = self._get_driver(driver)
        self.connection = driver.connect(*args, **kwargs)
        return self.connection

    def create_table(self, schema_class: DataSchema, table_name):
        create_table_query = self._create_table_string(schema=schema_class.__schema__, table_name=table_name)
        connection = self._get_connection()
        try:
            c = connection.cursor()
            c.execute(create_table_query)
        except sqlite3.Error as e:
            raise BackendException(str(e)) from e

    def save(self, data_obj: DataSchema, table_name):
        keys = []
        values = []
        for k, v in data_obj.__data__.items():
            keys.append(k)
            values.append(TYPE_PARSERS.get(type(v), lambda x: x)(v))
        query = f"insert into {table_name}({', '.join(keys)}) values ({', '.join(values)});"
        self._get_connection().cursor().execute(query)

    def select(self, schema_class: DataSchema, table_name: AnyStr, condition: Condition = None,
               limit: int = None, order_by=None, **kwargs):
        fields = ', '.join(schema_class.__signature__.parameters.keys())
        query = f'SELECT {fields} FROM {table_name}'
        if condition is not None:
            query += f' WHERE {self.get_sql_condition_string(condition)}'
        if limit is not None:
            query += f' LIMIT {limit}'
        if order_by is not None:
            query += f' ORDER BY {order_by.name}'
        query += ';'
        connection = self._get_connection()
        return SQLBackendResultIterator(
            schema_class=schema_class,
            result=connection.cursor().execute(query),
            fields=schema_class.__signature__.parameters.keys()
        )

    def _create_table_string(self, schema, table_name):
        fields = []
        for k, v in schema['properties'].items():
            field_str = f'{k} {TYPE_MAPPING[v["type"]]}'

            if k in schema.get('required', []):
                field_str += " NOT NULL"

            fields.append(field_str)
        query = "CREATE TABLE {} (\n\t{}\n);".format(table_name, ',\n\t'.join(fields))
        return query

    @classmethod
    def get_sql_condition_string(cls, c: Condition) -> AnyStr:
        a_str = None
        b_str = None

        if isinstance(c.a, fields.Field):
            a_str = c.a.name
        elif isinstance(c.a, Condition):
            a_str = f"({cls.get_sql_condition_string(c.a)})"

            if c.operator is operator.not_:
                return f"NOT ({cls.get_sql_condition_string(c.a)})"
        else:
            a_str = TYPE_PARSERS.get(type(c.a), lambda x: x)(c.a)

        if isinstance(c.b, fields.Field):
            b_str = c.b.name
        elif isinstance(c.b, Condition):
            b_str = f"({cls.get_sql_condition_string(c.b)})"
        else:
            b_str = TYPE_PARSERS.get(type(c.b), lambda x: x)(c.b)

        return f"{a_str} {SQL_OPERATOR_MAP[c.operator]} {b_str}"
