"""Interfaz gráfica de Compiscript con Streamlit.

Permite seleccionar un archivo .cps o escribir código directamente, ejecutar
el análisis léxico y sintáctico, y visualizar los errores, los tokens y el
árbol sintáctico.

Uso:
    streamlit run app.py
"""

import streamlit as st

from analisis import MENSAJE_EXITO, FilaError, ResultadoAnalisis, analizar_codigo
from lexico import Token

st.set_page_config(page_title="Compiscript — Analizador", page_icon="🔤", layout="wide")

st.title("Compiscript")
st.caption(
    "Analizador léxico y sintáctico del lenguaje Compiscript. "
    "Carga un archivo .cps o escribe tu código para detectar errores."
)


def _leer_archivo(uploaded) -> tuple[str, str | None, str | None]:
    """Decodifica el archivo subido y devuelve (nombre, contenido, error)."""
    try:
        codigo = uploaded.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        return uploaded.name, None, "El archivo no se pudo leer como texto UTF-8."
    return uploaded.name, codigo, None


def _tabla_de_tokens(tokens: list[Token]):
    """Tabla de tokens reconocidos en el formato que se muestra en la interfaz."""
    return [
        {"Línea": t.linea, "Columna": t.columna, "Tipo": t.tipo, "Lexema": t.lexema}
        for t in tokens
    ]


def _tabla_de_errores(errores: list[FilaError]):
    """Tabla de errores con el formato común exigido por la especificación."""
    return [
        {
            "Tipo": e.tipo,
            "Línea": e.linea,
            "Columna": e.columna,
            "Símbolo / Lexema": e.simbolo,
            "Descripción": e.descripcion,
        }
        for e in errores
    ]


def _mostrar_resultado(resultado: ResultadoAnalisis, codigo: str) -> None:
    st.divider()
    st.subheader("Resultado del análisis")

    if resultado.es_valido:
        st.success(MENSAJE_EXITO)
    else:
        st.error(
            f"Se encontraron {len(resultado.errores)} error(es) "
            "léxico(s) o sintáctico(s)."
        )
        st.dataframe(
            _tabla_de_errores(resultado.errores),
            width="stretch",
            hide_index=True,
        )

    with st.expander("Código analizado"):
        st.code(codigo, language="text")

    with st.expander(f"Tokens reconocidos ({len(resultado.tokens)})"):
        if resultado.tokens:
            st.dataframe(
                _tabla_de_tokens(resultado.tokens),
                width="stretch",
                hide_index=True,
            )
        else:
            st.write("No se reconoció ningún token.")

    with st.expander("Árbol sintáctico"):
        if resultado.arbol:
            st.code(resultado.arbol, language="text")
        else:
            st.write("No se pudo construir el árbol sintáctico.")


fuente = st.radio(
    "Fuente del código",
    ["Subir archivo .cps", "Escribir / pegar código"],
    horizontal=True,
)

nombre: str | None = None
codigo: str | None = None
mensaje_de_entrada: str | None = None

if fuente == "Subir archivo .cps":
    subido = st.file_uploader("Seleccionar archivo .cps", type=["cps"])
    if subido is not None:
        nombre, codigo, mensaje_de_entrada = _leer_archivo(subido)
else:
    codigo = st.text_area(
        "Escribe o pega aquí tu código Compiscript",
        height=250,
        placeholder="Ej.: let saludo: string = \"hola\";\nprint(saludo);",
    )
    nombre = "Código escrito"

if st.button("Analizar", type="primary"):
    if mensaje_de_entrada:
        st.error(mensaje_de_entrada)
    elif not codigo or not codigo.strip():
        st.warning("Escribe algún código Compiscript o selecciona un archivo .cps.")
    else:
        st.session_state["resultado"] = analizar_codigo(nombre or "Sin nombre", codigo)
        st.session_state["codigo"] = codigo

if "resultado" in st.session_state:
    _mostrar_resultado(st.session_state["resultado"], st.session_state["codigo"])
