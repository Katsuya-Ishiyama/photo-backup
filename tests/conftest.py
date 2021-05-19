import uuid

import pytest


@pytest.fixture(scope="function")
def test_folder():
    return uuid.uuid4()
