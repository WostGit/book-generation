from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ExperimentComponent:
    name: str
    kind: str
    settings: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RAGSource:
    kind: str
    path: str
    weight: float = 1.0


@dataclass(slots=True)
class ExperimentProfile:
    name: str
    model: ExperimentComponent
    embedding: ExperimentComponent
    reranker: ExperimentComponent
    retriever: ExperimentComponent
    prompt: ExperimentComponent
    genre: str
    chapter_count: int
    subchapters_per_chapter: int
    exports: list[str]
    validators: list[str]
    rag_sources: list[RAGSource] = field(default_factory=list)

    def run_key(self) -> str:
        payload = {
            "name": self.name,
            "model": self.model.name,
            "embedding": self.embedding.name,
            "reranker": self.reranker.name,
            "retriever": self.retriever.name,
            "prompt": self.prompt.name,
            "genre": self.genre,
            "chapter_count": self.chapter_count,
            "subchapters_per_chapter": self.subchapters_per_chapter,
            "exports": self.exports,
            "validators": self.validators,
            "rag": [f"{src.kind}:{src.path}:{src.weight}" for src in self.rag_sources],
        }
        return sha256(str(sorted(payload.items())).encode("utf-8")).hexdigest()[:16]


@dataclass(slots=True)
class RunProvenance:
    run_id: str
    profile: str
    started_at: str
    finished_at: str
    git_sha: str
    status: str
    cache_hit: bool
    metrics: dict[str, float]
    exports: dict[str, str]

    @classmethod
    def start(cls, run_id: str, profile: str, git_sha: str) -> "RunProvenance":
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            run_id=run_id,
            profile=profile,
            started_at=now,
            finished_at=now,
            git_sha=git_sha,
            status="running",
            cache_hit=False,
            metrics={},
            exports={},
        )

    def finalize(self, *, status: str, metrics: dict[str, float], exports: dict[str, Path]) -> None:
        self.finished_at = datetime.now(timezone.utc).isoformat()
        self.status = status
        self.metrics = metrics
        self.exports = {k: str(v) for k, v in exports.items()}
