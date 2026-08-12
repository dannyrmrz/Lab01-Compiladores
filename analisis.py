"""Análisis unificado (léxico + sintáctico) para la interfaz gráfica.

Corre los dos analizadores sobre el mismo código y junta sus errores en un
solo listado, ordenado por línea y columna y con un formato común listo para
mostrar en la interfaz:

    from analisis import analizar_codigo

    resultado = analizar_codigo("ejemplo.cps", codigo)
    resultado.es_valido    # True si no hubo errores léxicos ni sintácticos
    resultado.errores      # [FilaError(tipo, linea, columna, simbolo, descripcion), ...]
    resultado.tokens       # lista de Token (de lexico), para la tabla
    resultado.arbol        # árbol sintáctico como texto, para visualizarlo
"""

from dataclasses import dataclass, field

from generated.CompiscriptParser import CompiscriptParser
from lexico import Token, analizar_texto as analizar_texto_lexico
from sintactico import analizar_texto as analizar_texto_sintactico

# Mensaje que exige la especificación cuando el archivo no tiene errores.
MENSAJE_EXITO = (
    "El archivo se analizó correctamente: no se encontraron errores "
    "léxicos ni sintácticos."
)


@dataclass
class FilaError:
    """Un error (léxico o sintáctico) con el formato común de la interfaz."""

    tipo: str      # "Léxico" o "Sintáctico"
    linea: int
    columna: int
    simbolo: str   # Lexema o símbolo relacionado con el error.
    descripcion: str

    def __str__(self) -> str:
        return f"[{self.tipo}] Línea {self.linea}, columna {self.columna}: {self.descripcion}"


@dataclass
class ResultadoAnalisis:
    """Salida completa del análisis léxico y sintáctico de un código."""

    nombre: str
    errores: list[FilaError] = field(default_factory=list)
    tokens: list[Token] = field(default_factory=list)
    arbol: str = ""

    @property
    def es_valido(self) -> bool:
        """True si no se encontró ningún error léxico ni sintáctico."""
        return not self.errores


def analizar_codigo(nombre: str, codigo: str) -> ResultadoAnalisis:
    """Analiza código Compiscript con ambos analizadores y junta los errores."""
    lexico = analizar_texto_lexico(codigo)
    sintactico = analizar_texto_sintactico(codigo)

    errores = [
        FilaError("Léxico", e.linea, e.columna, e.lexema, e.descripcion)
        for e in lexico.errores
    ]
    errores += [
        FilaError("Sintáctico", e.linea, e.columna, e.simbolo, e.descripcion)
        for e in sintactico.errores
    ]
    errores.sort(key=lambda e: (e.linea, e.columna, e.tipo))

    arbol = (
        sintactico.arbol.toStringTree(ruleNames=CompiscriptParser.ruleNames)
        if sintactico.arbol is not None
        else ""
    )

    return ResultadoAnalisis(
        nombre=nombre,
        errores=errores,
        tokens=lexico.tokens,
        arbol=arbol,
    )
