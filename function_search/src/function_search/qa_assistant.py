from __future__ import annotations

from dataclasses import dataclass

from function_search.config import AppConfig
from function_search.lm_studio_client import LMStudioClient, LMStudioConfig, LMStudioError
from function_search.models import SearchResult
from function_search.prompts import SYSTEM_PROMPT
from function_search.search_engine import SearchEngine


@dataclass(slots=True)
class QAAnswer:
    question: str
    answer: str
    context_entries: list[SearchResult]


class QAAssistant:
    """Answer user questions using search context and a local LM Studio model."""

    def __init__(
        self,
        engine: SearchEngine,
        config: AppConfig | None = None,
        client: LMStudioClient | None = None,
    ) -> None:
        self._engine = engine
        self._config = config or AppConfig.load()
        self._client = client or LMStudioClient(
            LMStudioConfig(
                base_url=self._config.lm_studio_url,
                model=self._config.model,
                temperature=self._config.temperature,
                max_tokens=self._config.max_tokens,
                timeout=self._config.timeout,
            )
        )

    @property
    def config(self) -> AppConfig:
        return self._config

    @property
    def client(self) -> LMStudioClient:
        return self._client

    def is_available(self) -> bool:
        return self._client.is_server_running()

    def build_context(
        self,
        query: str,
        *,
        provider: str | None = None,
        limit: int | None = None,
    ) -> tuple[str, list[SearchResult]]:
        limit = limit or self._config.context_results
        results = self._engine.search(query, provider=provider, limit=limit)
        if not results:
            return "（未检索到相关 API）", []

        blocks: list[str] = []
        for index, result in enumerate(results, 1):
            entry = result.entry
            tags = ", ".join(entry.tags) if entry.tags else "-"
            block = (
                f"### [{index}] {entry.full_name}\n"
                f"- 来源: {entry.provider}\n"
                f"- 分类: {entry.category}\n"
                f"- 模块: {entry.module or '-'}\n"
                f"- 签名: {entry.signature or '-'}\n"
                f"- 标签: {tags}\n"
                f"- 说明: {entry.description or '（无）'}\n"
                f"- 示例:\n```\n{entry.example or '# 无示例'}\n```"
            )
            blocks.append(block)

        return "\n\n".join(blocks), results

    def answer(
        self,
        question: str,
        *,
        provider: str | None = None,
    ) -> QAAnswer:
        question = question.strip()
        if not question:
            raise ValueError("问题不能为空")

        context_text, results = self.build_context(question, provider=provider)
        user_message = (
            f"## 检索到的相关 API\n\n{context_text}\n\n"
            f"## 用户问题\n\n{question}"
        )
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        try:
            answer_text = self._client.chat(messages)
        except LMStudioError:
            raise

        return QAAnswer(
            question=question,
            answer=answer_text,
            context_entries=results,
        )
