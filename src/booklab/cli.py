from __future__ import annotations

import argparse
from pathlib import Path

from booklab.orchestration.runner import run_experiment
from booklab.reporting.leaderboard import generate_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="booklab")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run")
    run_p.add_argument("--experiment", type=Path, required=True)
    run_p.add_argument("--workspace", type=Path, required=True)
    run_p.add_argument("--fallback-mode", default="cpu", choices=["cpu", "gpu", "external-endpoint"])

    rep_p = sub.add_parser("report")
    rep_p.add_argument("--workspace", type=Path, required=True)
    rep_p.add_argument("--out", type=Path, required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "run":
        run_experiment(args.experiment, args.workspace, args.fallback_mode)
    elif args.command == "report":
        generate_reports(args.workspace, args.out)


if __name__ == "__main__":
    main()
