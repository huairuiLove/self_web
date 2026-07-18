from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class FunctionEntry:
    """A searchable API entry with documentation and example."""

    id: str
    provider: str
    category: str
    name: str
    full_name: str
    signature: str
    description: str
    example: str
    module: str = ""
    tags: list[str] = field(default_factory=list)

    def search_blob(self) -> str:
        """Concatenated text used for indexing and fuzzy matching."""
        parts = [
            self.name,
            self.full_name,
            self.category,
            self.module,
            self.signature,
            self.description,
            " ".join(self.tags),
        ]
        return " ".join(p for p in parts if p)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tags"] = list(self.tags)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FunctionEntry:
        return cls(
            id=data["id"],
            provider=data["provider"],
            category=data["category"],
            name=data["name"],
            full_name=data["full_name"],
            signature=data.get("signature", ""),
            description=data.get("description", ""),
            example=data.get("example", ""),
            module=data.get("module", ""),
            tags=list(data.get("tags", [])),
        )


@dataclass(slots=True)
class SearchResult:
    entry: FunctionEntry
    score: float
    match_reason: str = ""
