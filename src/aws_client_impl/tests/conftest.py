import pytest

@pytest.fixture(autouse=True)
def _no_network(socket_disabled):
    # If any test accidentally hits the network, it fails immediately.
    pass
