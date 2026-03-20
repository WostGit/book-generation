from __future__ import annotations

from pathlib import Path

from booklab.core.config import ConfigLoader
from booklab.orchestration.runner import ExperimentRunner


def test_pipeline_config_loads() -> None:
    root = Path(__file__).resolve().parents[1]
    config = ConfigLoader(root).load_pipeline()
    assert config.profiles
    assert any(model.id.startswith("qwen") for model in config.generation_models)


def test_runner_creates_artifacts() -> None:
    root = Path(__file__).resolve().parents[1]
    runner = ExperimentRunner(root)
    result = runner.run("fantasy-rag-smoke")
    run_dir = Path(result["run_dir"])
    assert (run_dir / "provenance.json").exists()
    assert (run_dir / "reports").exists()
    assert (run_dir / "exports").exists()
