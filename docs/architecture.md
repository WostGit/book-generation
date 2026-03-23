# Architecture Overview

BookLab separates concerns into five planes:

1. **Generation plane** (`generation/`): model adapters and runtime fallback modes.
2. **Retrieval plane** (`retrieval/`): RAG context assembly from local corpora.
3. **Evaluation plane** (`evaluation/`): heuristic + model-judge score APIs.
4. **Packaging plane** (`packaging/`, `plugins/`): multi-format exports and publisher checks.
5. **Orchestration plane** (`orchestration/`, CI workflow): matrix execution, resumability, provenance.

## Extensibility Contract

- New model/retriever/evaluator/exporter definitions are config objects in `configs/v1`.
- Plugins are Python classes under `booklab.plugins` and can be registered without orchestration edits.
- Experiment runs use content-addressed run IDs for dedupe and resumability.


## Standardized Book Shape

All experiment runs generate books with 5 chapters and 10 subchapters per chapter to normalize evaluation and leaderboard comparisons. Generated Markdown books are copied to `.artifacts/books` for quick inspection in CI artifacts.
