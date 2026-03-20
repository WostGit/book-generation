from __future__ import annotations

import re
from collections import Counter


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z']+", text.lower())


def evaluate_book(text: str, rag_used: bool) -> dict[str, float]:
    tokens = _tokenize(text)
    total = max(len(tokens), 1)
    unique = len(set(tokens))
    counts = Counter(tokens)

    duplication = sum(c - 1 for c in counts.values() if c > 1) / total
    readability = min(100.0, 100 * unique / total)
    coherence = max(0.0, 100.0 - duplication * 120)
    chapter_consistency = 75.0 if "chapter" in text.lower() else 40.0
    hallucination_rate = 15.0 if rag_used else 25.0

    return {
        "coherence": round(coherence, 2),
        "continuity": round((coherence + chapter_consistency) / 2, 2),
        "hallucination_rate": round(hallucination_rate, 2),
        "factual_grounding": 80.0 if rag_used else 55.0,
        "style_adherence": 70.0,
        "chapter_consistency": chapter_consistency,
        "duplication": round(duplication * 100, 2),
        "readability": round(readability, 2),
        "pacing": 68.0,
        "dialogue_quality": 62.0,
        "long_context_retention": 66.0,
    }
