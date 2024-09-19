import os
import tempfile

import pytest
from app import create_app
from app.db import get_db, init_db


@pytest.fixture
def app():
    """
    Creates and opens a temporary file, returning the file descriptor and the path to it.
    The DATABASE path is overridden so it points to this temporary path instead of the instance folder.
    After setting the path, the database tables are created and the test data is inserted.
    After the test is over, the temporary file is closed and removed.
    """
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Used for context to share across tests.
@pytest.fixture
def context():
    context = {}
    return context