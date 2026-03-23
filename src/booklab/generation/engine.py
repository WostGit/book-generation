from __future__ import annotations

from dataclasses import dataclass

from booklab.core.types import ExperimentComponent


@dataclass(slots=True)
class GenerationRequest:
    prompt: str
    model: ExperimentComponent
    chapter_count: int
    subchapters_per_chapter: int = 10
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
            subparts = []
            for sub_index in range(1, req.subchapters_per_chapter + 1):
                subparts.append(
                    f"### {index}.{sub_index} Subchapter\n"
                    f"Scene development for chapter {index}, subchapter {sub_index} using {model_family}."
                )
            chapters.append(
                f"## Chapter {index}\n"
                f"Generated narrative for chapter {index} using {model_family}.\n\n"
                + "\n\n".join(subparts)
            )
        return base + "\n\n".join(chapters)
