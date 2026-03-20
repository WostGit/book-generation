from __future__ import annotations

from pathlib import Path

from booklab.core.types import ExperimentProfile


class RAGContextBuilder:
    def build(self, profile: ExperimentProfile) -> str:
        if not profile.rag_sources:
            return ""

        snippets: list[str] = []
        for source in profile.rag_sources:
            path = Path(source.path)
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            snippets.append(f"[{source.kind}] {text[:800]}")
        return "\n\n".join(snippets)
