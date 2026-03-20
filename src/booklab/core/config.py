from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from booklab.core.types import ExperimentComponent, ExperimentProfile, RAGSource

try:
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None


class ConfigError(ValueError):
    pass


def load_document(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        if yaml is None:
            raise ConfigError("PyYAML is required to parse YAML files; use JSON configs in offline mode.")
        data = yaml.safe_load(raw)
    elif path.suffix == ".json":
        data = json.loads(raw)
    else:
        raise ConfigError(f"Unsupported config type: {path}")
    if not isinstance(data, dict):
        raise ConfigError(f"Config at {path} must be a mapping")
    return data


def load_component(path: Path, kind: str) -> ExperimentComponent:
    data = load_document(path)
    return ExperimentComponent(
        name=str(data.get("name", path.stem)),
        kind=kind,
        settings=dict(data.get("settings", {})),
    )


def _resolve(root: Path, rel: str) -> Path:
    direct = root / rel
    if direct.exists():
        return direct
    fallback = Path("configs/v1") / rel
    if fallback.exists():
        return fallback
    raise ConfigError(f"Unable to resolve config path: {rel}")


def load_experiment(path: Path, root: Path) -> ExperimentProfile:
    data = load_document(path)

    def comp(kind: str, key: str) -> ExperimentComponent:
        config_rel = data["components"][key]
        return load_component(_resolve(root, config_rel), kind)

    rag_sources = [RAGSource(**item) for item in data.get("rag_sources", [])]

    return ExperimentProfile(
        name=data["name"],
        model=comp("model", "model"),
        embedding=comp("embedding", "embedding"),
        reranker=comp("reranker", "reranker"),
        retriever=comp("retriever", "retriever"),
        prompt=comp("prompt", "prompt"),
        genre=data["scenario"]["genre"],
        chapter_count=int(data["scenario"]["chapter_count"]),
        exports=list(data["outputs"]["formats"]),
        validators=list(data["outputs"]["validators"]),
        rag_sources=rag_sources,
    )
