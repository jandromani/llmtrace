"""
LLMTrace: Un framework ligero de observabilidad y evaluación para aplicaciones con LLMs.

Este paquete proporciona herramientas para instrumentar interacciones con modelos de lenguaje,
almacenar trazas, métricas y feedback, y visualizar estos datos a través de un dashboard web
o la interfaz de línea de comandos.

Para empezar, llama a `llmtrace.init()` al inicio de tu aplicación.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Configurar el logger de LLMTrace
from llmtrace._logging import setup_logger
_log_format = os.getenv("LLMTRACE_LOG_FORMAT", "text").lower()
_json_format_default = _log_format == "json"
setup_logger(json_format=_json_format_default)

# Importar las funciones públicas para facilitar el acceso
from llmtrace.core.core import init, session, get_current_session_id, log_message, log_metric, add_feedback, log_error, get_sessions, get_messages, get_metrics, get_feedback, get_errors
from llmtrace.instrumentation.base import BaseInstrumentor
from llmtrace.instrumentation.openai import OpenAIInstrumentor
from llmtrace.instrumentation.huggingface import HFInstrumentor
from llmtrace.instrumentation.langchain import LangChainCallbackHandler
from llmtrace.storage.backends import StorageBackend
from llmtrace.tracing.models import Session, Message, Metric, Feedback, Error

# Función para cerrar la conexión a la base de datos
async def close():
    """
    Cierra la conexión activa a la base de datos de LLMTrace.
    Debe llamarse al finalizar la aplicación para asegurar que todos los datos
    se persistan correctamente y liberar recursos.
    """
    from llmtrace.core.core import _db_instance
    import logging
    logger = logging.getLogger("llmtrace")
    if _db_instance:
        await _db_instance.close()
        logger.info("LLMTrace database connection closed.")
    else:
        logger.warning("LLMTrace was not initialized or already closed.")

# Versión del paquete (se actualizará automáticamente con setuptools_scm)
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.0.0+unknown" # Fallback durante el desarrollo
