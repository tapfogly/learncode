import pytest


@pytest.fixture(scope='package', autouse=True)
def classFixture(rbk):
    print("初始化")
    yield
    print("清理")