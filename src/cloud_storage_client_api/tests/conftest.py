import pytest

@pytest.fixture(autouse=True)
def _no_network(socket_disabled):
    pass
