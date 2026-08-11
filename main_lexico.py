"""Prueba por consola del analizador léxico de Compiscript.

Uso:
    python main_lexico.py ejemplos/valido.cps
    python main_lexico.py ejemplos/con_errores.cps --tokens
"""

import sys

from lexico import analizar_archivo


def _imprimir_tokens(tokens) -> None:
    print(f"TOKENS RECONOCIDOS ({len(tokens)})")
    print(f"{'LÍNEA':>6} {'COL':>5}  {'TIPO':<16} LEXEMA")
    for t in tokens:
        print(f"{t.linea:>6} {t.columna:>5}  {t.tipo:<16} {t.lexema}")
    print()


def _imprimir_errores(errores) -> None:
    if not errores:
        print("El archivo se analizó correctamente: no se encontraron errores léxicos.")
        return
    print(f"ERRORES LÉXICOS ({len(errores)})")
    for error in errores:
        print(f"  {error}")


def main(argumentos: list[str]) -> int:
    if not argumentos:
        print("Uso: python main_lexico.py <archivo.cps> [--tokens]")
        return 1

    ruta = argumentos[0]
    try:
        resultado = analizar_archivo(ruta)
    except (OSError, ValueError) as e:
        print(f"No se pudo analizar el archivo: {e}")
        return 1

    print(f"Archivo: {ruta}\n")
    if "--tokens" in argumentos:
        _imprimir_tokens(resultado.tokens)
    _imprimir_errores(resultado.errores)
    return 0 if resultado.es_valido else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Tildes y ñ en la consola de Windows.
    sys.exit(main(sys.argv[1:]))
