from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

from booklab.core.contracts import EvaluationResult


@dataclass(slots=True)
class LeaderboardWriter:
    output_dir: Path

    def write(self, run_id: str, profile_id: str, evals: list[EvaluationResult]) -> list[Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        flattened: list[dict[str, float | str]] = []
        for result in evals:
            row: dict[str, float | str] = {"suite": result.suite_id}
            row.update(result.metrics)
            flattened.append(row)

        summary = {
            "run_id": run_id,
            "profile_id": profile_id,
            "rows": flattened,
            "aggregate": {
                metric: mean(
                    float(r[metric])
                    for r in flattened
                    if metric in r and isinstance(r[metric], (int, float))
                )
                for metric in {k for row in flattened for k in row if k != "suite"}
            },
        }

        json_path = self.output_dir / f"{run_id}_{profile_id}_summary.json"
        csv_path = self.output_dir / f"{run_id}_{profile_id}_leaderboard.csv"
        json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

        fieldnames = sorted({k for row in flattened for k in row})
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flattened)

        return [json_path, csv_path]
