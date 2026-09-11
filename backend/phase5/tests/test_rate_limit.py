from phase5.middleware.rate_limit import clear_rate_limits, is_rate_limited
from shared.config import settings


def test_rate_limit_blocks_after_threshold(monkeypatch):
    monkeypatch.setattr(settings, "rate_limit_requests", 3)
    monkeypatch.setattr(settings, "rate_limit_window_seconds", 60)
    clear_rate_limits()

    client = "127.0.0.1"
    assert is_rate_limited(client) is False
    assert is_rate_limited(client) is False
    assert is_rate_limited(client) is False
    assert is_rate_limited(client) is True


def test_rate_limit_is_per_client(monkeypatch):
    monkeypatch.setattr(settings, "rate_limit_requests", 1)
    monkeypatch.setattr(settings, "rate_limit_window_seconds", 60)
    clear_rate_limits()

    assert is_rate_limited("client-a") is False
    assert is_rate_limited("client-a") is True
    assert is_rate_limited("client-b") is False
