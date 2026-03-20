from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class PublisherCheckResult:
    target: str
    passed: bool
    message: str


class PublisherRulePlugin:
    target = "generic"

    def check(self, artifact_dir: Path) -> PublisherCheckResult:
        has_book = any(artifact_dir.glob("book.*"))
        return PublisherCheckResult(
            target=self.target,
            passed=has_book,
            message="Found at least one export file." if has_book else "No export file found.",
        )


class KDPPlugin(PublisherRulePlugin):
    target = "kdp"


class Draft2DigitalPlugin(PublisherRulePlugin):
    target = "draft2digital"


PLUGIN_REGISTRY = {
    "kdp": KDPPlugin,
    "draft2digital": Draft2DigitalPlugin,
    "ingramspark": PublisherRulePlugin,
    "kobo": PublisherRulePlugin,
    "lulu": PublisherRulePlugin,
    "gumroad": PublisherRulePlugin,
    "itchio": PublisherRulePlugin,
}
