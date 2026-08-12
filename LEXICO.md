# Analizador léxico de Compiscript

Escanea archivos `.cps`, entrega la lista de tokens reconocidos y reporta los
errores léxicos en español. El lexer no se escribió a mano: lo genera **ANTLR**
a partir de `Compiscript.g4`.

## Estructura

```
Compiscript.g4        Gramática
generated/            Lexer y parser que genera ANTLR.
lexico/errores.py     ErrorLexico + el ErrorListener que traduce y agrupa errores.
lexico/analizador.py  API pública: analizar_texto() y analizar_archivo().
main_lexico.py        Prueba por consola.
ejemplos/             Archivos .cps de prueba.
```

## Instalación y uso

```bash
pip install -r requirements.txt
```

```bash
python main_lexico.py ejemplos/con_errores.cps
```

Con `--tokens` se imprime además la tabla de tokens:

```bash
python main_lexico.py ejemplos/valido.cps --tokens
```

## API para la interfaz gráfica

```python
from lexico import analizar_archivo

resultado = analizar_archivo(ruta_elegida_en_la_gui)

resultado.es_valido   # True si no hubo errores léxicos
resultado.tokens      # [Token(tipo, lexema, linea, columna), ...]
resultado.errores     # [ErrorLexico(linea, columna, lexema, descripcion), ...]
```

`ErrorLexico` tiene el atributo `tipo == "Léxico"` y un `__str__` ya formateado,
por si conviene mostrarlo directo. `analizar_archivo` lanza `ValueError` si la
extensión no es `.cps` y `OSError` si el archivo no se puede leer. Para analizar
texto de un editor en memoria, existe `analizar_texto(codigo)`.

## Errores que detecta

| Caso | Mensaje |
|---|---|
| Carácter fuera del alfabeto (`@`, `$`) | carácter no reconocido por el lenguaje |
| Varios caracteres inválidos seguidos (`~~~`) | secuencia de caracteres no reconocida |
| Cadena sin comilla de cierre | cadena de texto sin cerrar |
| `'`, `&`, `\|`, `#` | mensaje con la sugerencia de la forma correcta |

De cada error se reporta tipo, línea, columna, lexema y descripción.

### Recuperación

El análisis **no se detiene en el primer error**: ANTLR descarta el carácter
conflictivo y continúa, así que una sola ejecución reporta todos los errores del
archivo. Como ANTLR emitiría un mensaje por cada carácter inválido, el colector
agrupa los caracteres inválidos contiguos en un único error para no repetir el
mismo mensaje. El descarte siempre avanza al menos un carácter, por lo que no
hay riesgo de ciclo infinito.

## Interfaz gráfica

Para seleccionar un archivo `.cps`, analizarlo y visualizar los tokens, los
errores y el árbol sintáctico, corre la interfaz con Streamlit:

```bash
streamlit run app.py
```

La interfaz ejecuta los analizadores léxico y sintáctico (vía `analisis.py`)
y junta sus errores en un solo listado.

## Regenerar desde la gramática

Solo hace falta si se modifica `Compiscript.g4`; los archivos de `generated/`
ya están en el repositorio.

```bash
antlr4 -v 4.13.2 -Dlanguage=Python3 -o generated Compiscript.g4
```
