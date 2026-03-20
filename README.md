# BookLab: Multi-Model RAG Book Generation Pipeline

BookLab is a highly modular, enterprise-style experimentation and packaging framework for long-form book generation.

## What this repository now supports

- **Config-first architecture**: models, retrievers, evaluators, exporters, publishers, and experiment matrices are declared in versioned YAML/JSON.
- **RAG-ready generation**: optional grounding from local corpora (knowledge bases, lore bibles, style guides, research packs, citation corpora).
- **Model-provider abstraction**: open-model adapters for Hugging Face-compatible instruct/reasoning checkpoints (Qwen, Llama, Mistral, Mixtral, DeepSeek, Phi, Gemma).
- **Execution fallbacks**: CPU, self-hosted GPU, or external endpoint mode flags.
- **Experiment orchestration**: profile-based runs with provenance manifests, cache keys, resumable artifact directories, and deterministic report outputs.
- **Packaging/export**: markdown/text/html/docx/odt/epub/pdf/rtf/fb2 artifact emission in one pass.
- **Quality evaluation**: heuristic evaluation suite covering coherence, continuity, hallucination proxy, style adherence, and long-context retention.
- **CI matrix strategy**: GitHub Actions matrix fan-out to stress profile/model combinations in parallel.
- **Publisher plugin surface**: KDP / Draft2Digital / IngramSpark / Kobo / Lulu / Gumroad / itch.io readiness checks scaffolded as config-driven targets.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python scripts/run_experiment.py --profile fantasy-rag-smoke
```

Artifacts are written to `artifacts/<run_id>/` with provenance, exports, and reports.

## Repository map

- `src/booklab/core`: typed contracts, config loader, plugin registry
- `src/booklab/providers`: model/embedding/reranker adapters
- `src/booklab/rag`: retrieval providers
- `src/booklab/evaluation`: evaluation suites
- `src/booklab/packaging`: multi-format exporters
- `src/booklab/reporting`: leaderboard/report writers
- `src/booklab/orchestration`: experiment runner
- `configs/**`: versioned declarations and matrix definitions
- `.github/workflows/book-lab.yml`: parallel CI orchestration

## Extending

1. Add plugin class implementing a core protocol.
2. Register plugin in `ExperimentRunner._register_builtin_plugins` or dynamic loader.
3. Add config entry under `configs/`.
4. Add/extend an experiment profile to include the plugin.

No hardcoded model IDs are required in runtime logic beyond plugin registration.
