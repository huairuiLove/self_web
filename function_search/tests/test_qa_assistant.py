from __future__ import annotations

from unittest.mock import MagicMock

from function_search.config import AppConfig
from function_search.lm_studio_client import LMStudioClient, LMStudioConfig
from function_search.models import FunctionEntry
from function_search.qa_assistant import QAAssistant
from function_search.search_engine import IndexBuilder, SearchEngine


def _sample_entry() -> FunctionEntry:
    return FunctionEntry(
        id="python:json.dumps",
        provider="python",
        category="function",
        name="dumps",
        full_name="json.dumps",
        signature="dumps(obj, *, indent=None) -> str",
        description="Serialize obj to a JSON formatted str.",
        example="json.dumps({'a': 1})",
        module="json",
        tags=["json", "serialize"],
    )


def test_build_context_includes_search_results(tmp_path) -> None:
    db = tmp_path / "test.db"
    IndexBuilder(db).build([_sample_entry()])
    engine = SearchEngine(db)
    engine.connect()

    assistant = QAAssistant(engine, AppConfig())
    context, results = assistant.build_context("json dumps")

    assert results
    assert "json.dumps" in context
    assert "Serialize obj" in context
    engine.close()


def test_answer_calls_lm_studio_with_prompt(tmp_path) -> None:
    db = tmp_path / "test.db"
    IndexBuilder(db).build([_sample_entry()])
    engine = SearchEngine(db)
    engine.connect()

    client = LMStudioClient(LMStudioConfig(model="test-model"))
    client.chat = MagicMock(return_value="使用 json.dumps 即可。")  # type: ignore[method-assign]

    assistant = QAAssistant(engine, AppConfig(), client=client)
    result = assistant.answer("怎么把 dict 转成 JSON 字符串？")

    assert result.answer == "使用 json.dumps 即可。"
    client.chat.assert_called_once()
    messages = client.chat.call_args.args[0]
    assert messages[0]["role"] == "system"
    assert "一次成型" in messages[0]["content"]
    assert "json.dumps" in messages[1]["content"]
    assert "怎么把 dict 转成 JSON 字符串？" in messages[1]["content"]
    engine.close()
