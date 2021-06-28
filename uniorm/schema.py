from dataclasses import dataclass
from inspect import Parameter, Signature, _empty
from typing import Any, AnyStr, Dict, List

import jsonschema

from .fields import TYPE_MAP


def make_signature(fields: List[AnyStr], required: List[AnyStr]) -> Signature:
    required_fields = []
    not_required_fields = []
    for name in fields:
        if name in required:
            required_fields.append(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD))
        else:
            not_required_fields.append(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD, default=None))
    return Signature(required_fields+not_required_fields)


class DataSchemaMeta(type):

    def __new__(cls, clsname, base, clsdict) -> Any:
        clsobj = super().__new__(cls, clsname, base, clsdict)
        if "properties" in clsobj.__schema__:
            sig = make_signature(clsobj.__schema__["properties"], clsobj.__schema__.get("required", []))
            setattr(clsobj, '__signature__', sig)

            for name, val in clsobj.__schema__["properties"].items():
                required = name in clsobj.__schema__.get("required", [])
                setattr(clsobj, name, TYPE_MAP[val['type']](name=name, required=required))

        return clsobj


class DataSchema(metaclass=DataSchemaMeta):
    __schema__: Dict = {}
    __tablename__: AnyStr = None
    __backend__ = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({', '.join([f'{k}={v}' for k,v in self.__data__.items()])})>"

    def __init__(self, *args, **kwargs) -> None:
        bound = self.__signature__.bind(*args, **kwargs)
        self.__data__ = {}

        for k, v in self.__signature__.parameters.items():
            if v.default is not _empty:
                setattr(self, k, v.default)
                self.__data__[k] = v.default

        for name, value in bound.arguments.items():
            setattr(self, name, value)
            self.__data__[name] = value

    @classmethod
    def create_table(cls):
        cls.__backend__.create_table(schema_class=cls, table_name=cls.__tablename__)

    @classmethod
    def select(cls, condition=None, limit=None, **kwargs):
        return cls.__backend__.select(schema_class=cls, table_name=cls.__tablename__, condition=condition, limit=limit, **kwargs)

    def save(self):
        return self.__backend__.save(self, self.__tablename__)


def create_dataclass(name: AnyStr, schema: Dict,  validator=None, backend=None, table_name=None) -> Any:
    _validator = validator if validator else jsonschema.Draft7Validator
    _validator.check_schema(schema)

    class ReturnedDataClass(DataSchema):
        __schema__: Dict = schema
        __backend__ = backend
        __tablename__ = table_name

    ReturnedDataClass.__qualname__ = name
    ReturnedDataClass.__name__ = name
    return ReturnedDataClass
