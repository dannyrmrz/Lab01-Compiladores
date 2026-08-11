"""Analizador léxico de Compiscript."""

from lexico.analizador import (
    EXTENSION,
    ResultadoLexico,
    Token,
    analizar_archivo,
    analizar_texto,
)
from lexico.errores import ErrorLexico

__all__ = [
    "EXTENSION",
    "ErrorLexico",
    "ResultadoLexico",
    "Token",
    "analizar_archivo",
    "analizar_texto",
]
