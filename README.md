> [!WARNING]
> **Historical alpha prototype (June 2025). Not production instrumentation.**
> The published OpenAI and Hugging Face example adapters currently wrap **mock provider classes**; they do not establish telemetry from real provider SDK calls. Tokens and costs in those examples are synthetic or illustrative. This repository has not been validated against current provider releases or independently audited for security/reliability. Treat screenshots as prototype illustrations, not live customer traces.
>
> For a real production integration, first replace mocks with supported SDK callbacks, add live-provider opt-in integration tests, secure prompt/PII handling, error/streaming support, and repeatable CI. This project remains in the historical archive rather than the flagship engineering showcase.

# LLMTrace: Observabilidad y Trazabilidad para Aplicaciones con LLM

**LLMTrace** es una librería open-source en Python diseñada como un toolkit de observabilidad y evaluación para aplicaciones con modelos de lenguaje. Permite a los desarrolladores instrumentar sus apps de IA generativa para registrar automáticamente prompts y respuestas, medir métricas clave y visualizar trazas de las sesiones.

[![SLSA Level 1](https://slsa.dev/images/gh-badge-level-1.svg)](https://slsa.dev)

## Características Principales (v0)

*   **Instrumentación Automática**: Captura prompts, respuestas, tokens, costos y errores de LLMs populares (OpenAI, HuggingFace, LangChain).
*   **Almacenamiento Local Persistente**: Utiliza SQLite por defecto para guardar todos los datos de trazabilidad. Soporte experimental para PostgreSQL.
*   **Dashboard Web Ligero**: Una interfaz web básica para visualizar sesiones y métricas.
*   **Interfaz de Línea de Comandos (CLI)**: Herramientas para listar, mostrar detalles, exportar y eliminar datos.
*   **Migraciones de Base de Datos**: Gestión de esquema con Alembic.

## Instalación

LLMTrace requiere Python 3.9 o superior.

1.  **Instalación básica:**
    \`\`\`bash
    pip install llmtrace
    \`\`\`

2.  **Instalación con extras (dashboard, evaluación, backends DB, instrumentadores):**
    \`\`\`bash
    pip install "llmtrace[all]" # Instala todas las dependencias opcionales
    # O selecciona solo las que necesites:
    # pip install "llmtrace[openai,postgresql]"
    \`\`\`

## Uso Rápido

```python
import llmtrace
from llmtrace.instrumentation.openai import OpenAIInstrumentor
import openai
import asyncio

async def main():
    # Inicializa LLMTrace (crea llmtrace.db en ~/.llmtrace por defecto)
    # Puedes usar LLMTRACE_DB_URL="memory://" para una base de datos en memoria para tests.
    await llmtrace.init() 
    
    # Instrumenta OpenAI
    OpenAIInstrumentor().instrument()

    # Todas las llamadas a openai.ChatCompletion.create serán registradas
    res = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Escribe un haiku sobre la observabilidad."}]
    )
    print(res.choices[0].message.content)

    # Inicia una sesión para agrupar trazas
    async with llmtrace.session(name="MiPrimerHaiku", user_id="anon_user"):
        await openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Otro haiku, esta vez sobre el código."}]
        )

    # Consulta datos programáticamente
    sessions = await llmtrace.get_sessions()
    print(f"\nSesiones registradas: {len(sessions)}")

    # Inicia el dashboard web
    # llmtrace web
    # Abre tu navegador en http://localhost:5000 (por defecto)
    
    await llmtrace.close() # Cierra la conexión a la DB
    
if __name__ == "__main__":
    asyncio.run(main())
