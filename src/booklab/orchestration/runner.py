from __future__ import annotations

import json
import subprocess
from dataclasses import asdict
from pathlib import Path

from booklab.core.config import load_experiment
from booklab.core.types import RunProvenance
from booklab.evaluation.metrics import evaluate_book
from booklab.generation.engine import GenerationEngine, GenerationRequest
from booklab.packaging.exporters import export_book, validate_exports
from booklab.plugins.publisher import PLUGIN_REGISTRY
from booklab.retrieval.rag import RAGContextBuilder

STANDARD_CHAPTER_COUNT = 5
STANDARD_SUBCHAPTER_COUNT = 10


def git_sha() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True)
            .strip()
        )
    except Exception:
        return "unknown"


def run_experiment(experiment_path: Path, workspace: Path, fallback_mode: str = "cpu") -> Path:
    profile = load_experiment(experiment_path, root=experiment_path.parent.parent)
    run_id = profile.run_key()
    run_dir = workspace / run_id
    done_flag = run_dir / "provenance.json"

    if done_flag.exists():
        return done_flag

    run_dir.mkdir(parents=True, exist_ok=True)
    prov = RunProvenance.start(run_id, profile.name, git_sha())

    rag_context = RAGContextBuilder().build(profile)
    prompt_text = profile.prompt.settings.get("template", "Generate a book")
    full_prompt = f"{prompt_text}\n\nGenre: {profile.genre}\n\n{rag_context}".strip()

    text = GenerationEngine().generate(
        GenerationRequest(
            prompt=full_prompt,
            model=profile.model,
            chapter_count=STANDARD_CHAPTER_COUNT,
            subchapter_count=STANDARD_SUBCHAPTER_COUNT,
            fallback_mode=fallback_mode,
        )
    )

    exports = export_book(text, run_dir / "exports", profile.exports)
    export_validity = validate_exports(exports)
    metrics = evaluate_book(text, rag_used=bool(profile.rag_sources))
    metrics.update({f"export_valid_{k}": float(v) for k, v in export_validity.items()})
    metrics["chapter_target"] = float(STANDARD_CHAPTER_COUNT)
    metrics["subchapter_target"] = float(STANDARD_SUBCHAPTER_COUNT)

    publisher_results: dict[str, bool] = {}
    for publisher_name in ["kdp", "draft2digital", "ingramspark", "kobo", "lulu", "gumroad", "itchio"]:
        plugin = PLUGIN_REGISTRY[publisher_name]()
        publisher_results[publisher_name] = plugin.check(run_dir / "exports").passed
    metrics.update({f"publisher_{k}": float(v) for k, v in publisher_results.items()})

    inspect_dir = workspace / "books"
    inspect_dir.mkdir(parents=True, exist_ok=True)
    inspect_book = inspect_dir / f"{profile.name}-{run_id}.md"
    inspect_book.write_text(text, encoding="utf-8")

    prov.finalize(status="success", metrics=metrics, exports=exports)
    done_flag.write_text(json.dumps(asdict(prov), indent=2), encoding="utf-8")
    return done_flag
