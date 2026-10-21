"""Verify the published adapter's actual, deliberately simulated boundary."""

import pytest

import llmtrace
from llmtrace.instrumentation.openai import (
    OpenAIInstrumentor,
    mock_openai,
)
from llmtrace.storage.sqlite import SQLiteBackend


@pytest.mark.asyncio
async def test_mock_adapter_records_a_local_session_and_restores_itself(tmp_path):
    SQLiteBackend._instance = None
    await llmtrace.init(str(tmp_path / "mock-demo.db"))
    original = mock_openai.ChatCompletion.create
    adapter = OpenAIInstrumentor()
    adapter.instrument()
    try:
        async with llmtrace.session(name="simulated") as session_id:
            response = await mock_openai.ChatCompletion.create(
                model="demo-model",
                messages=[{"role": "user", "content": "local fixture"}],
            )
            assert response["choices"][0]["message"]["content"].startswith(
                "This is a mock response"
            )
            messages = await llmtrace.get_messages(session_id)
            assert [message.role for message in messages] == ["user", "assistant"]
        assert len(await llmtrace.get_sessions()) == 1
    finally:
        adapter.uninstrument()
        await llmtrace.close()
        SQLiteBackend._instance = None
    assert mock_openai.ChatCompletion.create == original
