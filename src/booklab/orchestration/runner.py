from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from uuid import uuid4

from booklab.core.config import ConfigLoader, ExperimentProfile, PipelineConfig
from booklab.core.contracts import BookRequest, EvaluationResult
from booklab.core.registry import PluginRegistry
from booklab.evaluation.heuristics import HeuristicEvaluator
from booklab.packaging.exporters import MultiFormatExporter
from booklab.providers.embedding import SimpleEmbeddingAdapter
from booklab.providers.open_model import OpenModelAdapter
from booklab.providers.reranker import SimpleReranker
from booklab.rag.retrievers import LocalCorpusRetriever
from booklab.reporting.leaderboard import LeaderboardWriter


@dataclass(slots=True)
class ExperimentRunner:
    repo_root: Path
    loader: ConfigLoader = field(init=False)
    models: PluginRegistry = field(init=False)
    embeddings: PluginRegistry = field(init=False)
    rerankers: PluginRegistry = field(init=False)
    retrievers: PluginRegistry = field(init=False)
    evaluators: PluginRegistry = field(init=False)
    exporters: PluginRegistry = field(init=False)

    def __post_init__(self) -> None:
        self.loader = ConfigLoader(self.repo_root)
        self.models = PluginRegistry()
        self.embeddings = PluginRegistry()
        self.rerankers = PluginRegistry()
        self.retrievers = PluginRegistry()
        self.evaluators = PluginRegistry()
        self.exporters = PluginRegistry()
        self._register_builtin_plugins()

    def _register_builtin_plugins(self) -> None:
        self.models.register("hf-open-model", lambda cfg: OpenModelAdapter(**cfg))
        self.embeddings.register("simple-embedding", lambda cfg: SimpleEmbeddingAdapter(**cfg))
        self.rerankers.register("simple-reranker", lambda cfg: SimpleReranker(**cfg))
        self.retrievers.register("local-corpus", lambda cfg: LocalCorpusRetriever(**cfg))
        self.evaluators.register("heuristics", lambda cfg: HeuristicEvaluator(**cfg))
        self.exporters.register("multiformat", lambda cfg: MultiFormatExporter(**cfg))

    def run(self, profile_id: str) -> dict[str, str]:
        config = self.loader.load_pipeline()
        profile = self._resolve_profile(config, profile_id)
        run_id = uuid4().hex[:12]
        run_dir = self.repo_root / "artifacts" / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        manifest = {"run_id": run_id, "profile": asdict(profile)}
        (run_dir / "provenance.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")

        evaluations: list[EvaluationResult] = []
        for genre in profile.genres:
            for chapter_count in profile.chapter_counts:
                request = BookRequest(
                    title=f"{genre.title()} Prototype {chapter_count}",
                    genre=genre,
                    chapter_count=chapter_count,
                    prompt_template_id=profile.prompt_template,
                    profile_id=profile.id,
                    rag_enabled=profile.retrieval.enabled,
                )
                draft = self._generate(config, profile, request)
                self._export(config, profile, draft, run_dir)
                evaluations.extend(self._evaluate(config, profile, draft))

        report_dir = run_dir / "reports"
        files = LeaderboardWriter(report_dir).write(run_id=run_id, profile_id=profile.id, evals=evaluations)
        return {"run_id": run_id, "run_dir": str(run_dir), "report_files": ",".join(map(str, files))}

    def _resolve_profile(self, config: PipelineConfig, profile_id: str) -> ExperimentProfile:
        for profile in config.profiles:
            if profile.id == profile_id:
                return profile
        msg = f"Unknown profile '{profile_id}'"
        raise KeyError(msg)

    def _generate(self, config: PipelineConfig, profile: ExperimentProfile, request: BookRequest):
        model_ref = next(m for m in config.generation_models if m.id == profile.generation_model)
        model = self.models.create(model_ref.plugin, model_ref.params)

        retrieval_context = None
        if profile.retrieval.enabled and profile.retrieval.retriever_id:
            retriever_ref = next(r for r in config.retrievers if r.id == profile.retrieval.retriever_id)
            retriever = self.retrievers.create(retriever_ref.plugin, retriever_ref.params)
            retrieval_context = retriever.retrieve(request.genre, top_k=profile.retrieval.top_k)

        cache_key = hashlib.sha256(
            f"{profile.id}:{request.genre}:{request.chapter_count}:{bool(retrieval_context)}".encode("utf-8")
        ).hexdigest()[:16]
        request.metadata["cache_key"] = cache_key
        return model.generate(request, retrieval_context)

    def _export(self, config: PipelineConfig, profile: ExperimentProfile, draft, run_dir: Path) -> None:
        target_dir = run_dir / "exports"
        for export_id in profile.export_targets:
            export_ref = next(e for e in config.exporters if e.id == export_id)
            exporter = self.exporters.create(export_ref.plugin, export_ref.params)
            exporter.export(draft, str(target_dir))

    def _evaluate(self, config: PipelineConfig, profile: ExperimentProfile, draft) -> list[EvaluationResult]:
        results: list[EvaluationResult] = []
        for evaluator_id in profile.validation_suites:
            eval_ref = next(e for e in config.evaluators if e.id == evaluator_id)
            evaluator = self.evaluators.create(eval_ref.plugin, eval_ref.params)
            results.append(evaluator.evaluate(draft))
        return results
