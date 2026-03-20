from __future__ import annotations

from dataclasses import dataclass

from booklab.core.contracts import Reranker


@dataclass(slots=True)
class SimpleReranker(Reranker):
    reranker_id: str

    def rerank(self, query: str, candidates: list[str]) -> list[str]:
        return sorted(candidates, key=lambda c: abs(len(c) - len(query)))
