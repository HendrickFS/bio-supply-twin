import pytest


# Minimal pytest configuration for async tests
@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'
