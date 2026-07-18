from __future__ import annotations

from pathlib import Path

from function_search.providers.base import Provider
from function_search.providers.json_provider import JsonDataProvider
from function_search.providers.pytorch_provider import PyTorchProvider

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def get_all_providers(*, include_pytorch: bool = True) -> list[Provider]:
    providers: list[Provider] = []

    if include_pytorch:
        providers.append(PyTorchProvider())

    providers.extend(
        [
            JsonDataProvider(
                "python",
                "Python 常用",
                _DATA_DIR / "python_common.json",
            ),
            JsonDataProvider(
                "backend",
                "Python 后端开发",
                _DATA_DIR / "backend_common.json",
            ),
        ]
    )
    return providers


def get_runtime_providers() -> list[Provider]:
    """Providers that do not require optional build-time dependencies."""
    return [
        JsonDataProvider(
            "python",
            "Python 常用",
            _DATA_DIR / "python_common.json",
        ),
        JsonDataProvider(
            "backend",
            "Python 后端开发",
            _DATA_DIR / "backend_common.json",
        ),
    ]
