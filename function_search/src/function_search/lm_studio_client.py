from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class LMStudioError(RuntimeError):
    """Raised when LM Studio API calls fail."""


@dataclass(slots=True)
class LMStudioConfig:
    base_url: str = "http://localhost:1234/v1"
    model: str = ""
    api_key: str = "lm-studio"
    temperature: float = 0.3
    max_tokens: int = 2048
    timeout: float = 180.0


class LMStudioClient:
    """Minimal OpenAI-compatible client for the local LM Studio server."""

    def __init__(self, config: LMStudioConfig | None = None) -> None:
        self.config = config or LMStudioConfig()

    @property
    def _base(self) -> str:
        return self.config.base_url.rstrip("/")

    def is_server_running(self) -> bool:
        try:
            self.list_models()
            return True
        except LMStudioError:
            return False

    def list_models(self) -> list[dict[str, Any]]:
        data = self._request("GET", "/models")
        return list(data.get("data", []))

    def resolve_model_id(self) -> str:
        if self.config.model:
            return self.config.model
        models = self.list_models()
        if not models:
            raise LMStudioError("LM Studio 未加载任何模型，请先在 LM Studio 中加载模型")
        return str(models[0].get("id", ""))

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self.resolve_model_id(),
            "messages": messages,
            "temperature": temperature if temperature is not None else self.config.temperature,
            "max_tokens": max_tokens if max_tokens is not None else self.config.max_tokens,
            "stream": False,
        }
        data = self._request("POST", "/chat/completions", payload=payload)
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise LMStudioError(f"无法解析 LM Studio 响应: {data}") from exc

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self._base}{path}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
        }
        body = None
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise LMStudioError(f"LM Studio HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise LMStudioError(
                f"无法连接 LM Studio ({self._base})，请确认已启动本地服务器"
            ) from exc

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LMStudioError(f"LM Studio 返回了无效 JSON: {raw[:200]}") from exc
