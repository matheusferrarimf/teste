"""Pequenos componentes reaproveitados entre as paginas."""

import streamlit as st

from servicos.pontuacao import pontos_da_questao

from .estilo import CORES


def etiqueta(texto: str, estilo: str = "") -> str:
    classe = f"av-tag {estilo}".strip()
    return f'<span class="{classe}">{texto}</span>'


def badge_peso(questao: dict) -> str:
    visual = questao["tipo_questao"] == "visual"
    rotulo = "codigo em execucao" if visual else "teorica"
    pontos = pontos_da_questao(questao["peso"])
    return etiqueta(
        f"{rotulo} · peso {questao['peso']} · {pontos} pts",
        "" if visual else "cinza",
    )


def kpi(rotulo: str, valor: str, alerta: bool = False) -> None:
    classe = "av-kpi-val alerta" if alerta else "av-kpi-val"
    fundo = CORES["amber_soft"] if alerta else CORES["surface"]
    borda = "#F0D0A8" if alerta else CORES["line"]
    st.markdown(
        f'<div class="av-card" style="background:{fundo};border-color:{borda}">'
        f'<div class="av-kpi-rot">{rotulo}</div>'
        f'<div class="{classe}">{valor}</div></div>',
        unsafe_allow_html=True,
    )


def medida(nota: float) -> str:
    """Barra de cinco segmentos usada nas medias do dashboard."""
    blocos = []
    for n in range(1, 6):
        if nota >= n - 0.5:
            blocos.append('<span class="cheio"></span>')
        elif nota >= n - 1:
            blocos.append('<span class="meio"></span>')
        else:
            blocos.append("<span></span>")
    return f'<div class="av-medida">{"".join(blocos)}</div>'


def cartao(conteudo_html: str, destaque: bool = False) -> None:
    classe = "av-card destaque" if destaque else "av-card"
    st.markdown(f'<div class="{classe}">{conteudo_html}</div>', unsafe_allow_html=True)
