from __future__ import annotations

import json
from pathlib import Path


def load_extension_providers(extensions_dir: Path) -> list:
    """Load custom providers from user extensions directory."""
    from function_search.providers.json_provider import JsonDataProvider

    providers = []
    if not extensions_dir.exists():
        return providers

    for path in sorted(extensions_dir.glob("*.json")):
        if path.name.endswith(".meta.json"):
            continue
        meta_file = path.with_suffix(".meta.json")
        provider_id = path.stem
        display_name = provider_id
        if meta_file.exists():
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            provider_id = meta.get("id", provider_id)
            display_name = meta.get("display_name", display_name)

        providers.append(JsonDataProvider(provider_id, display_name, path))
    return providers
