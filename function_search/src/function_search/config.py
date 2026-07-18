from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from function_search.paths import user_data_dir

DEFAULT_LM_STUDIO_URL = "http://localhost:1234/v1"
DEFAULT_MODEL = "glm-4-32b-0414"
DEFAULT_CONTEXT_RESULTS = 8
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TIMEOUT = 180.0


@dataclass
class AppConfig:
    lm_studio_url: str = DEFAULT_LM_STUDIO_URL
    model: str = DEFAULT_MODEL
    context_results: int = DEFAULT_CONTEXT_RESULTS
    temperature: float = DEFAULT_TEMPERATURE
    max_tokens: int = DEFAULT_MAX_TOKENS
    timeout: float = DEFAULT_TIMEOUT

    @classmethod
    def load(cls, path: Path | None = None) -> AppConfig:
        config_path = path or (user_data_dir() / "config.json")
        if not config_path.exists():
            return cls()
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            known = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
            return cls(**known)
        except (json.JSONDecodeError, TypeError, ValueError):
            return cls()

    def save(self, path: Path | None = None) -> None:
        config_path = path or (user_data_dir() / "config.json")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            json.dumps(asdict(self), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
