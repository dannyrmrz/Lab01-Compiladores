# Analizador sintáctico de Compiscript

Parsea la secuencia de tokens (a partir de la regla `program`) y reporta los
errores sintácticos en español. El parser tampoco se escribió a mano: lo
genera **ANTLR** a partir de `Compiscript.g4`, igual que el lexer.

## Estructura

```
generated/               Lexer y parser que genera ANTLR (compartido con lexico/).
sintactico/errores.py    ErrorSintactico + el ErrorListener que traduce los errores.
sintactico/analizador.py API pública: analizar_texto() y analizar_archivo().
main_sintactico.py       Prueba por consola.
ejemplos/                Archivos .cps de prueba.
```

## Instalación y uso

```bash
pip install -r requirements.txt
```

```bash
python main_sintactico.py ejemplos/con_errores_sintacticos.cps
```

Con `--arbol` se imprime además el árbol sintáctico (notación con paréntesis):

```bash
python main_sintactico.py ejemplos/valido.cps --arbol
```

## API para la interfaz gráfica

```python
from sintactico import analizar_archivo

resultado = analizar_archivo(ruta_elegida_en_la_gui)

resultado.es_valido   # True si no hubo errores sintácticos
resultado.arbol       # ParserRuleContext de 'program' (útil a futuro para el análisis semántico)
resultado.errores     # [ErrorSintactico(linea, columna, simbolo, descripcion), ...]
```

`ErrorSintactico` tiene el atributo `tipo == "Sintáctico"` y un `__str__` ya
formateado, por si conviene mostrarlo directo. `analizar_archivo` lanza
`ValueError` si la extensión no es `.cps` y `OSError` si el archivo no se
puede leer. Para analizar texto de un editor en memoria, existe
`analizar_texto(codigo)`.

Nota: `sintactico.analizar_texto` no reporta errores léxicos (de eso se
encarga `lexico.analizar_texto`); simplemente descarta los caracteres
inválidos y sigue, para no imprimir nada duplicado en consola. La interfaz
gráfica debe correr ambos análisis y juntar las dos listas de errores.

## Cómo se arma el mensaje de cada error

ANTLR entrega el símbolo que causó el error (`offendingSymbol`) y, en ese
mismo punto, el conjunto de tokens que sí eran válidos
(`recognizer.getExpectedTokens()`). El módulo traduce ambos datos a una
frase en español, por ejemplo:

```
[Sintáctico] Línea 5, columna 1: se encontró 'let', lo cual no es válido aquí; se esperaba ;
[Sintáctico] Línea 19, columna 5: se encontró 'return', lo cual no es válido aquí; se esperaba {
```

Si el conjunto esperado es muy grande (puede pasar dentro de una expresión,
donde caben muchas alternativas), se listan hasta 6 opciones y se indica
cuántas más hay, en vez de imprimir una lista enorme.

### Recuperación

El análisis **no se detiene en el primer error**: se usa el
`DefaultErrorStrategy` de ANTLR, que ante un error intenta primero insertar o
descartar un solo token (por ejemplo, un `;` faltante) y, si no lo logra,
salta al siguiente punto de sincronización (el fin de la regla actual, por
ejemplo el cierre de un bloque) y continúa el parseo desde ahí. Así, una sola
ejecución reporta varios errores en vez de detenerse en el primero.

Para evitar mensajes repetidos en cascada cuando ANTLR reintenta varias veces
en el mismo punto, el colector ignora un error si tiene exactamente la misma
línea, columna y símbolo que el anterior.

## Interfaz gráfica

La interfaz con Streamlit (`app.py`) selecciona un archivo `.cps` o acepta
código pegado, ejecuta el análisis léxico y sintáctico, y muestra los errores
de ambos tipos en una sola tabla, además de los tokens y el árbol sintáctico.

```bash
streamlit run app.py
```

## Regenerar desde la gramática

Solo hace falta si se modifica `Compiscript.g4`; los archivos de `generated/`
ya están en el repositorio (compartidos entre `lexico` y `sintactico`).

```bash
antlr4 -v 4.13.2 -Dlanguage=Python3 -o generated Compiscript.g4
```
