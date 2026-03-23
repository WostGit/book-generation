# BookLab: Multi-Model RAG Book Generation Pipeline

BookLab is a modular, enterprise-style experimentation pipeline for end-to-end book generation, retrieval grounding (RAG), quality evaluation, and multi-format packaging.

## Design Goals

> Default standardization: every run emits **5 chapters x 10 subchapters** for apples-to-apples inspection.

- **Config-first architecture**: models, retrievers, judges, exporters, validators, and experiment profiles are versioned YAML/JSON files.
- **Plugin-friendly**: add components without touching orchestration core.
- **Parallelizable CI**: GitHub Actions matrix stress-tests the full workflow.
- **Resumable runs**: deterministic run IDs, cache-aware dedupe, and per-run provenance logs.
- **RAG-native**: optional grounding using knowledge bases, style guides, lore bibles, and citation corpora.
- **Publishing-ready outputs**: markdown/txt/html/docx/odt/epub/pdf/rtf/fb2 validators and packaging checks.

## Quick Start

```bash
python -m pip install -e .[dev]
booklab run --experiment configs/v1/experiments/baseline.json --workspace .artifacts
booklab report --workspace .artifacts --out .artifacts/leaderboard
```

## Repository Layout

- `src/booklab/core`: typed configuration, registry, and provenance models.
- `src/booklab/generation`: generator abstractions and local/external fallbacks.
- `src/booklab/retrieval`: RAG context builders + retriever provider interfaces.
- `src/booklab/evaluation`: heuristic and judge-style metric pipeline.
- `src/booklab/packaging`: exporters, validators, publisher packaging checks.
- `src/booklab/orchestration`: experiment execution, caching, resumability.
- `src/booklab/reporting`: CSV/JSON/Markdown leaderboards.
- `configs/v1`: versioned component and experiment profiles.
- `.github/workflows`: matrix CI orchestration.

## Adding New Ideas with Config + Plugins

1. Drop a config file in `configs/v1/<category>/`.
2. Implement a plugin under `src/booklab/plugins/` (if behavior is new).
3. Reference plugin/config in an experiment profile.
4. Run `booklab run --experiment <profile>`.

## CI Matrix Dimensions

Workflow matrix can vary these knobs in parallel:

- generation model family
- embedding model
- reranker
- chunking strategy
- retriever provider + settings
- prompt template
- genre + chapter count
- export target
- validation suite

## Notes

- Integrations with HF/vLLM/TGI/OpenAI-compatible endpoints are adapter-driven and optional.
- Publisher upload automation is intentionally **not** included; only readiness checks and packaging hooks are provided.
