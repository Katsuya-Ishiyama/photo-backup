import sys

import pytest


@pytest.fixture(scope="function")
def folder_test():
    return "test/python-{}.{}".format(*sys.version_info[:2])
