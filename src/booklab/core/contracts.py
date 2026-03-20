from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(slots=True)
class BookRequest:
    title: str
    genre: str
    chapter_count: int
    prompt_template_id: str
    profile_id: str
    rag_enabled: bool
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BookDraft:
    request: BookRequest
    chapters: list[str]
    citations: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RetrievalContext:
    chunks: list[str]
    sources: list[str]


@dataclass(slots=True)
class EvaluationResult:
    suite_id: str
    metrics: dict[str, float]
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ArtifactRecord:
    path: str
    kind: str
    metadata: dict[str, Any] = field(default_factory=dict)


class GenerationModel(Protocol):
    model_id: str

    def generate(self, request: BookRequest, context: RetrievalContext | None = None) -> BookDraft:
        ...


class EmbeddingModel(Protocol):
    model_id: str

    def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class Reranker(Protocol):
    reranker_id: str

    def rerank(self, query: str, candidates: list[str]) -> list[str]:
        ...


class Retriever(Protocol):
    retriever_id: str

    def retrieve(self, query: str, top_k: int = 8) -> RetrievalContext:
        ...


class Evaluator(Protocol):
    evaluator_id: str

    def evaluate(self, draft: BookDraft) -> EvaluationResult:
        ...


class Exporter(Protocol):
    export_id: str

    def export(self, draft: BookDraft, output_dir: str) -> list[ArtifactRecord]:
        ...
