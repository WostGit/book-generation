from pathlib import Path

from booklab.core.config import load_experiment
from booklab.orchestration.runner import run_experiment
from booklab.packaging.exporters import SUPPORTED_FORMATS
from booklab.reporting.leaderboard import generate_reports


def test_load_experiment() -> None:
    path = Path("configs/v1/experiments/baseline.json")
    profile = load_experiment(path, root=path.parent.parent)
    assert profile.name == "baseline-enterprise-rag"
    assert profile.chapter_count == 6
    assert "pdf" in profile.exports


def test_runner_and_reports(tmp_path: Path) -> None:
    exp = Path("configs/v1/experiments/lightweight.json")
    prov = run_experiment(exp, tmp_path)
    assert prov.exists()

    books = list((tmp_path / "books").glob("*.md"))
    assert books
    text = books[0].read_text(encoding="utf-8")
    assert text.count("## Chapter") == 5
    assert text.count("###") == 50

    out = tmp_path / "reports"
    reports = generate_reports(tmp_path, out)
    assert reports["json"].exists()
    assert reports["csv"].exists()
    assert reports["markdown"].exists()


def test_supported_formats_cover_requested_targets() -> None:
    required = {"md", "txt", "html", "docx", "odt", "epub", "pdf", "rtf", "fb2"}
    assert required.issubset(SUPPORTED_FORMATS)
