# LLMTRACE · historical alpha

This repository is a June 2025 Python prototype for local session storage, metrics and a Flask dashboard. **The published OpenAI and Hugging Face adapters wrap mock provider classes.** They do not intercept the current provider SDKs. The token and cost values shown in examples are illustrative; this is not production instrumentation.

The repository is retained as a technical archive. Before using it for real workloads, the adapters need real SDK integration, opt-in integration tests, privacy controls for prompt data, streaming and failure handling, and a passing cross-platform test suite.

## What is in the repository

- SQLite-backed sessions, messages, metrics, feedback and errors; experimental PostgreSQL backend.
- A local Flask dashboard and a command-line interface.
- Mock provider adapters used to explore trace shape and storage behavior.
- Source and tests that can be inspected independently of the screenshots.

## Local demonstration

Requires Python 3.10 or later. Create an isolated environment and install the package:

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
```

The following example records a simulated call. It makes **no network request to OpenAI**:

```python
import asyncio
import llmtrace
from llmtrace.instrumentation.openai import OpenAIInstrumentor, mock_openai

async def main():
    await llmtrace.init("demo-llmtrace.db")
    instrumentor = OpenAIInstrumentor()
    instrumentor.instrument()
    try:
        async with llmtrace.session(name="Mock demonstration", user_id="demo"):
            result = await mock_openai.ChatCompletion.create(
                model="demo-model",
                messages=[{"role": "user", "content": "Hello from a local demo"}],
            )
            print(result["choices"][0]["message"]["content"])
        print("Sessions:", len(await llmtrace.get_sessions()))
    finally:
        instrumentor.uninstrument()
        await llmtrace.close()

asyncio.run(main())
```

Run `pytest` for the repository tests. Their result, if passing, validates the implemented fixtures and local behavior; it does not validate real provider telemetry.

## Project status and license

Version 0.1.4 is an alpha. The repository code is MIT licensed; see [LICENSE](LICENSE). Third-party attribution is recorded in [LICENSE-THIRD-PARTY.md](LICENSE-THIRD-PARTY.md). A PyPI release, CI badge or provenance level must not be inferred from this README; inspect the [workflow history](https://github.com/jandromani/llmtrace/actions) and [PyPI project](https://pypi.org/project/llmtrace/) separately.
