import os
import tempfile

import pytest

from poultry import app


@pytest.fixture
def client():
    db_fd, poultry.app.config['DATABASE'] = tempfile.mkstemp()
    poultry.app.config['TESTING'] = True

    with poultry.app.test_client() as client:
        with poultry.app.app_context():
            poultry.init_db()
        yield client

    os.close(db_fd)
    os.unlink(poultry.app.config['DATABASE'])