import tempfile

import pytest


@pytest.fixture(scope='function')
def sqlite3_file():
    with tempfile.NamedTemporaryFile(suffix='.db') as file:
        yield file
