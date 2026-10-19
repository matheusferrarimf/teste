"""Questionario de avaliacao do prototipo, aplicado ao final da rodada."""

import time

import streamlit as st

from componentes.estilo import titulo
from dados import repositorio
from servicos.analise import CRITERIOS
from servicos.pontuacao import pontuacao_maxima


def _resumo(rodada: dict) -> None:
    total = len(rodada["questoes"])
    tempos = rodada["tempos"] or [0]
    maximo = pontuacao_maxima(rodada["questoes"])

    st.markdown('<div class="av-eyebrow">Sessao concluida</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Pontuacao", f"{rodada['pontos']} de {maximo}")
    col2.metric("Acertos", f"{rodada['acertos']} de {total}")
    col3.metric("Tempo medio", f"{sum(tempos) / len(tempos):.0f}s por questao")


def render() -> None:
    rodada = st.session_state.get("rodada")
    if not rodada:
        st.session_state.tela = "inicio"
        st.rerun()
        return

    if "inicio_avaliacao" not in st.session_state:
        st.session_state.inicio_avaliacao = time.time()

    _resumo(rodada)
    st.divider()

    titulo(
        "Avalie o prototipo",
        apoio="Suas respostas sao usadas apenas para a pesquisa deste trabalho de "
              "conclusao de curso.",
    )

    with st.form("avaliacao"):
        notas = {}
        for chave, rotulo, pergunta in CRITERIOS:
            notas[chave] = st.select_slider(
                pergunta, options=[1, 2, 3, 4, 5], value=3, key=f"nota_{chave}"
            )
        st.caption("1 = discordo totalmente · 5 = concordo totalmente")

        comentario = st.text_area(
            "Algo que voce mudaria na ferramenta? (opcional)", placeholder="Escreva aqui."
        )
        enviado = st.form_submit_button("Enviar avaliacao", type="primary")

    if enviado:
        segundos = int(time.time() - st.session_state.inicio_avaliacao)
        repositorio.salvar_avaliacao(
            rodada["id_sessao"], notas, comentario.strip(), segundos
        )
        st.session_state.rodada = None
        st.session_state.pop("inicio_avaliacao", None)
        st.session_state.tela = "dashboard"
        st.rerun()
