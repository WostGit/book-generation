from __future__ import annotations

from dataclasses import dataclass

from booklab.core.contracts import BookDraft, EvaluationResult, Evaluator


@dataclass(slots=True)
class HeuristicEvaluator(Evaluator):
    evaluator_id: str

    def evaluate(self, draft: BookDraft) -> EvaluationResult:
        chapter_lengths = [len(ch) for ch in draft.chapters]
        coherence = min(1.0, sum(chapter_lengths) / (len(chapter_lengths) * 400.0)) if chapter_lengths else 0.0
        continuity = 1.0 - (max(chapter_lengths) - min(chapter_lengths)) / max(chapter_lengths, default=1)
        hallucination_proxy = 0.2 if draft.citations else 0.6
        metrics = {
            "coherence": round(coherence, 3),
            "continuity": round(max(0.0, continuity), 3),
            "hallucination_proxy": round(hallucination_proxy, 3),
            "style_adherence": 0.75,
            "long_context_retention": 0.7,
        }
        return EvaluationResult(suite_id=self.evaluator_id, metrics=metrics)
