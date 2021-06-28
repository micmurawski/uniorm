from uniorm import create_dataclass
from uniorm.backends import SQLBackend


def test_sql_backend(sqlite3_file):
    schema = {
        "$schema": "https://json-schema.org/schema#",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
        },
        "required": ["email"]
    }

    backend = SQLBackend()
    backend.create_connection('sqlite3', sqlite3_file.name)
    Person = create_dataclass(name='Person', schema=schema, backend=backend, table_name='person_table_1')
    Person.create_table()
    person1 = Person(email='mmmurawski777@gmail.com')
    person1.save()
    person2 = Person(name='Jon', email='jon@wp.pl')
    person2.save()

    condition1 = (Person.name.is_not(None))
    condition2 = (Person.email == 'jon@wp.pl')

    condition3 = condition1 & condition2

    result = list(Person.select(condition3, order_by=Person.email))
    assert len(result) == 1
    assert result[0].name == person2.name
    assert result[0].email == person2.email
