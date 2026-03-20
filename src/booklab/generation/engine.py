from __future__ import annotations

from dataclasses import dataclass

from booklab.core.types import ExperimentComponent


@dataclass(slots=True)
class GenerationRequest:
    prompt: str
    model: ExperimentComponent
    chapter_count: int
    fallback_mode: str = "cpu"


class GenerationEngine:
    """Adapter-style generation engine.

    This is intentionally lightweight and can be extended with concrete integrations
    (transformers, vLLM, TGI, OpenAI-compatible endpoints) without changing callers.
    """

    def generate(self, req: GenerationRequest) -> str:
        model_family = req.model.settings.get("family", req.model.name)
        base = (
            f"# {req.prompt}\n\n"
            f"Model: {model_family} | Mode: {req.fallback_mode}\n\n"
        )
        chapters = []
        for index in range(1, req.chapter_count + 1):
            chapters.append(
                f"## Chapter {index}\n"
                f"Generated narrative for chapter {index} using {model_family}."
            )
        return base + "\n\n".join(chapters)
