from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


Factory = Callable[[dict[str, Any]], Any]


@dataclass(slots=True)
class PluginRegistry:
    """String-keyed registry for models, retrievers, evaluators, and exporters."""

    _factories: dict[str, Factory] = field(default_factory=dict)

    def register(self, key: str, factory: Factory) -> None:
        if key in self._factories:
            msg = f"Plugin key '{key}' is already registered"
            raise ValueError(msg)
        self._factories[key] = factory

    def create(self, key: str, config: dict[str, Any]) -> Any:
        if key not in self._factories:
            known = ", ".join(sorted(self._factories)) or "<none>"
            msg = f"Unknown plugin '{key}'. Known: {known}"
            raise KeyError(msg)
        return self._factories[key](config)

    def keys(self) -> list[str]:
        return sorted(self._factories)
