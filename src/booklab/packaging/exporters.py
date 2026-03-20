from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from booklab.core.contracts import ArtifactRecord, BookDraft, Exporter


@dataclass(slots=True)
class MultiFormatExporter(Exporter):
    export_id: str
    extensions: list[str]

    def export(self, draft: BookDraft, output_dir: str) -> list[ArtifactRecord]:
        destination = Path(output_dir)
        destination.mkdir(parents=True, exist_ok=True)
        artifacts: list[ArtifactRecord] = []
        full_text = "\n\n".join(draft.chapters)
        for ext in self.extensions:
            filename = f"{draft.request.title.replace(' ', '_').lower()}.{ext}"
            path = destination / filename
            path.write_text(full_text, encoding="utf-8")
            artifacts.append(ArtifactRecord(path=str(path), kind=ext))
        return artifacts
