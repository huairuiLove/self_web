from __future__ import annotations

from function_search.providers.base import Provider


class ProviderRegistry:
    """Runtime registry for dynamically adding search providers."""

    def __init__(self) -> None:
        self._providers: dict[str, Provider] = {}

    def register(self, provider: Provider) -> None:
        self._providers[provider.id] = provider

    def unregister(self, provider_id: str) -> None:
        self._providers.pop(provider_id, None)

    def get(self, provider_id: str) -> Provider | None:
        return self._providers.get(provider_id)

    def all(self) -> list[Provider]:
        return list(self._providers.values())

    def display_names(self) -> dict[str, str]:
        return {p.id: p.display_name for p in self._providers.values()}
