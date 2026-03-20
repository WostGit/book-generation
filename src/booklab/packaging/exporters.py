from __future__ import annotations

from pathlib import Path

SUPPORTED_FORMATS = {"md", "txt", "html", "docx", "odt", "epub", "pdf", "rtf", "fb2"}


class ExportError(ValueError):
    pass


def export_book(text: str, out_dir: Path, formats: list[str]) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, Path] = {}

    for fmt in formats:
        if fmt not in SUPPORTED_FORMATS:
            raise ExportError(f"Unsupported export format: {fmt}")

        path = out_dir / f"book.{fmt}"
        if fmt == "html":
            path.write_text(f"<html><body><pre>{text}</pre></body></html>", encoding="utf-8")
        elif fmt == "fb2":
            path.write_text(f"<FictionBook><body>{text}</body></FictionBook>", encoding="utf-8")
        else:
            path.write_text(text, encoding="utf-8")
        outputs[fmt] = path

    return outputs


def validate_exports(exports: dict[str, Path]) -> dict[str, bool]:
    results: dict[str, bool] = {}
    for fmt, path in exports.items():
        exists = path.exists() and path.stat().st_size > 0
        has_extension = path.suffix == f".{fmt}"
        results[fmt] = exists and has_extension
    return results
