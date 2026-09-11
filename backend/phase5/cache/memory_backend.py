from typing import Any

_MEMORY: dict[str, Any] = {}


def memory_get(key: str) -> Any | None:
    return _MEMORY.get(key)


def memory_set(key: str, value: Any) -> None:
    _MEMORY[key] = value


def memory_clear() -> None:
    _MEMORY.clear()
