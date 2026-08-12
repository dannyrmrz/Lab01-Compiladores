"""Analizador sintáctico de Compiscript."""

from sintactico.analizador import (
    EXTENSION,
    ResultadoSintactico,
    analizar_archivo,
    analizar_texto,
)
from sintactico.errores import ErrorSintactico

__all__ = [
    "EXTENSION",
    "ErrorSintactico",
    "ResultadoSintactico",
    "analizar_archivo",
    "analizar_texto",
]
