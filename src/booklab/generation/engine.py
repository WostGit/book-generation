from __future__ import annotations

from dataclasses import dataclass

from booklab.core.types import ExperimentComponent


@dataclass(slots=True)
class GenerationRequest:
    prompt: str
    model: ExperimentComponent
    chapter_count: int
    subchapter_count: int
    fallback_mode: str = "cpu"


class GenerationEngine:
    """Adapter-style generation engine.

    This is intentionally lightweight and can be extended with concrete integrations
    (transformers, vLLM, TGI, OpenAI-compatible endpoints) without changing callers.
    """

    def generate(self, req: GenerationRequest) -> str:
        model_family = req.model.settings.get("family", req.model.name)
        parts = [
            f"# {req.prompt}",
            f"Model: {model_family} | Mode: {req.fallback_mode}",
            f"Structure: {req.chapter_count} chapters x {req.subchapter_count} subchapters",
        ]

        for chapter in range(1, req.chapter_count + 1):
            parts.append(f"\n## Chapter {chapter}\n")
            for subchapter in range(1, req.subchapter_count + 1):
                parts.append(
                    f"### {chapter}.{subchapter} Subchapter\n"
                    f"Generated narrative for chapter {chapter}, subchapter {subchapter} using {model_family}."
                )

        return "\n\n".join(parts)
