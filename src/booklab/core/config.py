from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class PluginRef:
    id: str
    plugin: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RagProfile:
    enabled: bool = False
    retriever_id: str | None = None
    top_k: int = 8
    corpora: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ExperimentProfile:
    id: str
    generation_model: str
    embedding_model: str
    reranker: str
    prompt_template: str
    chunker: str
    retrieval: RagProfile
    genres: list[str]
    chapter_counts: list[int]
    export_targets: list[str]
    validation_suites: list[str]


@dataclass(slots=True)
class PipelineConfig:
    generation_models: list[PluginRef]
    embedding_models: list[PluginRef]
    rerankers: list[PluginRef]
    retrievers: list[PluginRef]
    evaluators: list[PluginRef]
    exporters: list[PluginRef]
    profiles: list[ExperimentProfile]


class ConfigLoader:
    def __init__(self, root: Path) -> None:
        self.root = root

    def load_json(self, relative_path: str) -> dict[str, Any]:
        path = self.root / relative_path
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            msg = f"Expected mapping in {path}"
            raise ValueError(msg)
        return data

    def load_pipeline(self, manifest: str = "configs/pipeline.json") -> PipelineConfig:
        payload = self.load_json(manifest)

        def refs(key: str) -> list[PluginRef]:
            return [PluginRef(**item) for item in payload.get(key, [])]

        profiles: list[ExperimentProfile] = []
        for profile in payload.get("profiles", []):
            rag = RagProfile(**profile.get("retrieval", {}))
            profiles.append(
                ExperimentProfile(
                    id=profile["id"],
                    generation_model=profile["generation_model"],
                    embedding_model=profile["embedding_model"],
                    reranker=profile["reranker"],
                    prompt_template=profile["prompt_template"],
                    chunker=profile["chunker"],
                    retrieval=rag,
                    genres=list(profile.get("genres", [])),
                    chapter_counts=list(profile.get("chapter_counts", [])),
                    export_targets=list(profile.get("export_targets", [])),
                    validation_suites=list(profile.get("validation_suites", [])),
                )
            )

        return PipelineConfig(
            generation_models=refs("generation_models"),
            embedding_models=refs("embedding_models"),
            rerankers=refs("rerankers"),
            retrievers=refs("retrievers"),
            evaluators=refs("evaluators"),
            exporters=refs("exporters"),
            profiles=profiles,
        )
