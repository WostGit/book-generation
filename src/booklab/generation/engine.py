from __future__ import annotations

from dataclasses import dataclass

from booklab.core.types import ExperimentComponent


@dataclass(slots=True)
class GenerationRequest:
    prompt: str
    model: ExperimentComponent
    chapter_count: int = 5
    subchapter_count: int = 10
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
            f"Model: {model_family} | Mode: {req.fallback_mode}\n"
            f"Structure: {req.chapter_count} chapters x {req.subchapter_count} subchapters\n\n"
        )
        chapters = []
        for index in range(1, req.chapter_count + 1):
            subchapters = []
            for sub in range(1, req.subchapter_count + 1):
                subchapters.append(
                    f"### {index}.{sub} Subchapter\n"
                    f"Narrative segment {sub} in chapter {index}, generated with {model_family}."
                )
            chapters.append(f"## Chapter {index}\n\n" + "\n\n".join(subchapters))
        return base + "\n\n".join(chapters)
