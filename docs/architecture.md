# Architecture Overview

## Separation of concerns

- **Generation**: `providers/open_model.py`
- **Retrieval (RAG)**: `rag/retrievers.py`
- **Evaluation**: `evaluation/heuristics.py`
- **Packaging/export**: `packaging/exporters.py`
- **Reporting**: `reporting/leaderboard.py`
- **Orchestration/CI binding**: `orchestration/runner.py` and `.github/workflows/book-lab.yml`

## Experiment lifecycle

1. Load versioned config manifest.
2. Resolve profile and matrix dimensions.
3. Build plugin instances from registry.
4. Retrieve context when RAG is enabled.
5. Generate chapter draft.
6. Export into many formats.
7. Evaluate with multiple suites.
8. Emit provenance + leaderboard artifacts.

## Future plugin extension points

- vector DB integrations (Qdrant / Milvus / pgvector)
- LLM judges for advanced evaluation
- publisher package compliance suites
- conversion validators (EPUBCheck, PDF/A rules)
