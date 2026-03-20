from __future__ import annotations

from dataclasses import dataclass

from booklab.core.contracts import EmbeddingModel


@dataclass(slots=True)
class SimpleEmbeddingAdapter(EmbeddingModel):
    model_id: str

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(text) % 97), float(sum(ord(ch) for ch in text) % 101)] for text in texts]
