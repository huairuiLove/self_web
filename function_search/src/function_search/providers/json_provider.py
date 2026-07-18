from __future__ import annotations

import json
from pathlib import Path

from function_search.models import FunctionEntry
from function_search.providers.base import Provider


class JsonDataProvider(Provider):
    """Loads curated function entries from a JSON dataset."""

    def __init__(self, provider_id: str, display_name: str, data_file: Path) -> None:
        self._id = provider_id
        self._display_name = display_name
        self.data_file = data_file

    @property
    def id(self) -> str:
        return self._id

    @property
    def display_name(self) -> str:
        return self._display_name

    def collect(self) -> list[FunctionEntry]:
        if not self.data_file.exists():
            raise FileNotFoundError(f"Dataset not found: {self.data_file}")

        raw = json.loads(self.data_file.read_text(encoding="utf-8"))
        entries: list[FunctionEntry] = []
        for item in raw:
            full_name = item["full_name"]
            entries.append(
                FunctionEntry(
                    id=f"{self._id}:{full_name}",
                    provider=self._id,
                    category=item.get("category", "function"),
                    name=item["name"],
                    full_name=full_name,
                    signature=item.get("signature", full_name),
                    description=item.get("description", ""),
                    example=item.get("example", ""),
                    module=item.get("module", ""),
                    tags=item.get("tags", []),
                )
            )
        return entries
