"""Questionario de avaliacao do prototipo, aplicado ao final da visita.

Uma visita pode ter varios modulos concluidos. A avaliacao continua ligada
a uma unica sessao no banco (avaliacao 1 : 0..1 sessao): a da ultima
sessao concluida.
"""

import html
import time

import streamlit as st

from componentes.estilo import CORES, titulo
from dados import repositorio
from servicos.analise import CRITERIOS
from servicos.pontuacao import resumir_visita


def _resumo(sessoes: list) -> None:
    visita = resumir_visita(sessoes)

    rotulo = "Modulo concluido" if len(sessoes) == 1 else f"{len(sessoes)} modulos concluidos"
    st.markdown(f'<div class="av-eyebrow">{rotulo}</div>', unsafe_allow_html=True)
    for s in sessoes:
        st.markdown(
            f'<div style="font-size:14px;color:{CORES["ink2"]};padding:2px 0">'
            f'<strong style="color:{CORES["ink"]}">{html.escape(s["nome_conteudo"])}</strong> · '
            f'{s["pontos"]} de {s["maximo"]} pts · {s["acertos"]} de {s["total"]} acertos'
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("")
    col1, col2, col3 = st.columns(3)
    col1.metric("Pontuacao da visita", f"{visita['pontos']} de {visita['maximo']}")
    col2.metric("Acertos", f"{visita['acertos']} de {visita['total']}")
    col3.metric("Tempo medio", f"{visita['tempo_medio']:.0f}s por questao")


def render() -> None:
    sessoes = st.session_state.get("sessoes_concluidas") or []
    if not sessoes:
        st.session_state.tela = "inicio"
        st.rerun()
        return

    if "inicio_avaliacao" not in st.session_state:
        st.session_state.inicio_avaliacao = time.time()

    _resumo(sessoes)
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
            sessoes[-1]["id_sessao"], notas, comentario.strip(), segundos
        )
        # Limpar o apelido reabre o pop-up de identificacao para o proximo
        # aluno que usar o mesmo computador do laboratorio.
        st.session_state.sessoes_concluidas = []
        st.session_state.pop("inicio_avaliacao", None)
        st.session_state.apelido = ""
        st.session_state.rodada = None
        st.session_state.tela = "inicio"
        # O toast e exibido pela tela inicial: chamado aqui, sumiria no rerun.
        st.session_state.agradecer = True
        st.rerun()
