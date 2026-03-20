from __future__ import annotations

from dataclasses import dataclass, field

from booklab.core.contracts import RetrievalContext, Retriever


@dataclass(slots=True)
class LocalCorpusRetriever(Retriever):
    retriever_id: str
    corpora: dict[str, list[str]] = field(default_factory=dict)

    def retrieve(self, query: str, top_k: int = 8) -> RetrievalContext:
        chunks: list[str] = []
        sources: list[str] = []
        for source, docs in self.corpora.items():
            for paragraph in docs:
                if query.lower()[:12] in paragraph.lower() or len(chunks) < top_k:
                    chunks.append(paragraph)
                    sources.append(source)
                if len(chunks) >= top_k:
                    break
            if len(chunks) >= top_k:
                break
        return RetrievalContext(chunks=chunks, sources=sources)
