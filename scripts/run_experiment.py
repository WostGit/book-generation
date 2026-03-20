from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from booklab.orchestration.runner import ExperimentRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a book lab experiment profile")
    parser.add_argument("--profile", required=True, help="Profile id from configs/pipeline.json")
    args = parser.parse_args()

    runner = ExperimentRunner(REPO_ROOT)
    result = runner.run(args.profile)
    print(result)


if __name__ == "__main__":
    main()
