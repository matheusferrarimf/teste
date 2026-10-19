"""Tema visual: fundo claro com azul institucional UNIDAVI."""

import streamlit as st

CORES = {
    "bg": "#F4F7FB",
    "surface": "#FFFFFF",
    "ink": "#0C1B2A",
    "ink2": "#3D5266",
    "muted": "#5F7186",
    "line": "#DCE6F2",
    "blue": "#0A4C93",
    "blue_deep": "#073A72",
    "blue_bright": "#1B72D0",
    "blue_soft": "#E7F0FB",
    "ok": "#137A56",
    "ok_soft": "#E3F5ED",
    "bad": "#B32B21",
    "bad_soft": "#FCEBE9",
    "amber": "#B06A00",
    "amber_soft": "#FDF1DF",
    "gray": "#93A3B5",
}

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

.stApp {{ background: {CORES['bg']}; }}
html, body, [class*="css"] {{ font-family: 'IBM Plex Sans', system-ui, sans-serif; }}
h1, h2, h3 {{ font-family: 'Space Grotesk', system-ui, sans-serif !important;
              color: {CORES['ink']} !important; letter-spacing: -0.02em; }}

/* eyebrow acima dos titulos */
.av-eyebrow {{ font-family: 'IBM Plex Mono', monospace; font-size: 11px;
               letter-spacing: 0.12em; color: {CORES['blue_bright']};
               font-weight: 600; text-transform: uppercase; }}

/* etiquetas */
.av-tag {{ display: inline-flex; align-items: center; gap: 5px; border-radius: 999px;
           padding: 4px 10px; font-family: 'IBM Plex Mono', monospace; font-size: 11px;
           font-weight: 600; background: {CORES['blue_soft']}; color: {CORES['blue']};
           margin-right: 6px; }}
.av-tag.cinza {{ background: #F0F3F7; color: {CORES['muted']}; }}
.av-tag.ambar {{ background: {CORES['amber_soft']}; color: {CORES['amber']}; }}
.av-tag.verde {{ background: {CORES['ok_soft']}; color: {CORES['ok']}; }}

/* trilho de visualizacao — elemento assinatura */
.av-trilho {{ background: #FBFDFF; border: 1px solid {CORES['line']}; border-radius: 12px;
              padding: 20px 18px 10px; }}
.av-barras {{ display: flex; align-items: flex-end; justify-content: center; gap: 8px;
              height: 200px; }}
.av-col {{ display: flex; flex-direction: column; align-items: center; width: 54px; }}
.av-cel {{ width: 100%; display: flex; align-items: flex-end; justify-content: center;
           border-radius: 6px; border: 1.5px solid; padding-bottom: 8px;
           font-family: 'IBM Plex Mono', monospace; font-size: 15px; font-weight: 600;
           transition: all .25s ease; }}
.av-regua {{ display: flex; justify-content: center; gap: 8px; margin-top: 8px;
             border-top: 1px solid {CORES['line']}; padding-top: 6px; }}
.av-idx {{ width: 54px; text-align: center; font-family: 'IBM Plex Mono', monospace;
           font-size: 11px; color: {CORES['gray']}; }}
.av-idx.ativo {{ color: {CORES['blue']}; font-weight: 700; }}

/* legenda do passo */
.av-legenda {{ margin-top: 12px; border-radius: 8px; padding: 12px 16px;
               background: {CORES['blue_soft']}; border: 1px solid #C9DDF3; }}
.av-legenda .rot {{ font-family: 'IBM Plex Mono', monospace; font-size: 10px;
                    letter-spacing: 0.1em; color: {CORES['blue_bright']}; font-weight: 600; }}
.av-legenda .txt {{ font-size: 14px; color: {CORES['ink']}; margin-top: 2px; }}

/* cartoes */
.av-card {{ background: {CORES['surface']}; border: 1px solid {CORES['line']};
            border-radius: 12px; padding: 18px 20px; }}
.av-card.destaque {{ border-left: 3px solid {CORES['blue']}; }}
.av-kpi-rot {{ font-size: 12px; color: {CORES['muted']}; }}
.av-kpi-val {{ font-family: 'Space Grotesk', sans-serif; font-size: 30px; font-weight: 700;
               color: {CORES['ink']}; line-height: 1.1; }}
.av-kpi-val.alerta {{ color: {CORES['amber']}; }}

/* botoes */
.stButton > button {{ border-radius: 8px; font-family: 'IBM Plex Sans', sans-serif;
                      font-weight: 600; border: 1px solid {CORES['line']}; }}
.stButton > button[kind="primary"] {{ background: {CORES['blue']};
                                      border-color: {CORES['blue']}; }}

/* barra de medias do dashboard */
.av-medida {{ display: flex; gap: 4px; margin-top: 6px; }}
.av-medida span {{ flex: 1; height: 10px; border-radius: 3px; background: {CORES['line']}; }}
.av-medida span.cheio {{ background: {CORES['blue']}; }}
.av-medida span.meio {{ background: #9CC3EC; }}

@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>
"""


def aplicar() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def titulo(texto: str, eyebrow: str = "", apoio: str = "") -> None:
    if eyebrow:
        st.markdown(f'<div class="av-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.markdown(f"## {texto}")
    if apoio:
        st.markdown(
            f'<p style="color:{CORES["muted"]};font-size:14px;max-width:620px;'
            f'margin-top:-8px">{apoio}</p>',
            unsafe_allow_html=True,
        )
