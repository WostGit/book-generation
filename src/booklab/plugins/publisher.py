from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PublisherReadinessPlugin:
    plugin_id: str

    def validate(self, package_manifest: dict[str, str], checks: list[str]) -> dict[str, bool]:
        return {check: bool(package_manifest.get(check, "ok")) for check in checks}
