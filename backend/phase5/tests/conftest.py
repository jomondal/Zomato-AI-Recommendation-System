import pytest

from phase5.cache.manager import clear_cache
from phase5.cache.redis_backend import reset_redis_client
from phase5.middleware.rate_limit import clear_rate_limits


@pytest.fixture(autouse=True)
def reset_production_state():
    clear_cache()
    clear_rate_limits()
    reset_redis_client()
    yield
    clear_cache()
    clear_rate_limits()
    reset_redis_client()
