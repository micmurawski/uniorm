from uniorm.schema import DataSchema


class BackendException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class Backend:
    pass


class BackendResultIterator:
    def __init__(self, schema_class: DataSchema, result, fields=None) -> None:
        self.schema_class = schema_class
        self.result = result
        self.fields = fields

    def __iter__(self):
        return self
