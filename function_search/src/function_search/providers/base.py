from __future__ import annotations

from abc import ABC, abstractmethod

from function_search.models import FunctionEntry


class Provider(ABC):
    """Base class for extensible API data providers."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique provider identifier, e.g. 'pytorch'."""

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable provider name."""

    @abstractmethod
    def collect(self) -> list[FunctionEntry]:
        """Return all searchable entries from this provider."""
