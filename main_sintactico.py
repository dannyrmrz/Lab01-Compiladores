"""Prueba por consola del analizador sintáctico de Compiscript.

Uso:
    python main_sintactico.py ejemplos/valido.cps
    python main_sintactico.py ejemplos/con_errores.cps --arbol
"""

import sys

from generated.CompiscriptParser import CompiscriptParser
from sintactico import analizar_archivo


def _imprimir_arbol(arbol) -> None:
    print("ÁRBOL SINTÁCTICO")
    print(arbol.toStringTree(ruleNames=CompiscriptParser.ruleNames))
    print()


def _imprimir_errores(errores) -> None:
    if not errores:
        print("El archivo se analizó correctamente: no se encontraron errores sintácticos.")
        return
    print(f"ERRORES SINTÁCTICOS ({len(errores)})")
    for error in errores:
        print(f"  {error}")


def main(argumentos: list[str]) -> int:
    if not argumentos:
        print("Uso: python main_sintactico.py <archivo.cps> [--arbol]")
        return 1

    ruta = argumentos[0]
    try:
        resultado = analizar_archivo(ruta)
    except (OSError, ValueError) as e:
        print(f"No se pudo analizar el archivo: {e}")
        return 1

    print(f"Archivo: {ruta}\n")
    if "--arbol" in argumentos:
        _imprimir_arbol(resultado.arbol)
    _imprimir_errores(resultado.errores)
    return 0 if resultado.es_valido else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Tildes y ñ en la consola de Windows.
    sys.exit(main(sys.argv[1:]))
