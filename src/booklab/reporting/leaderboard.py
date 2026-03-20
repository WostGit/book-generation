from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def _collect(workspace: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for file in workspace.glob("*/provenance.json"):
        items.append(json.loads(file.read_text(encoding="utf-8")))
    return items


def generate_reports(workspace: Path, out_dir: Path) -> dict[str, Path]:
    records = _collect(workspace)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "summary.json"
    json_path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    csv_path = out_dir / "summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["run_id", "profile", "status", "coherence", "factual_grounding"])
        for record in records:
            metrics = record.get("metrics", {})
            writer.writerow(
                [
                    record.get("run_id"),
                    record.get("profile"),
                    record.get("status"),
                    metrics.get("coherence"),
                    metrics.get("factual_grounding"),
                ]
            )

    md_path = out_dir / "leaderboard.md"
    rows = ["| Run | Profile | Coherence | Grounding |", "|---|---|---:|---:|"]
    for record in sorted(records, key=lambda r: r.get("metrics", {}).get("coherence", 0), reverse=True):
        m = record.get("metrics", {})
        rows.append(
            f"| {record.get('run_id')} | {record.get('profile')} | {m.get('coherence', 0)} | {m.get('factual_grounding', 0)} |"
        )
    md_path.write_text("\n".join(rows), encoding="utf-8")

    return {"json": json_path, "csv": csv_path, "markdown": md_path}
