"""Tela inicial: identificacao do estudante e escolha do conteudo."""

import html

import streamlit as st

from componentes.dialogos import dialogo_identificacao
from componentes.estilo import CORES, titulo
from componentes.fluxo import iniciar_rodada
from componentes.ui import etiqueta
from dados import repositorio
from servicos.pontuacao import PESOS, PONTOS_POR_PESO


def _identificacao(apelido: str) -> None:
    """Linha discreta no topo com o apelido atual e a opcao de troca.

    A troca fica bloqueada depois de concluir um modulo: as sessoes ja
    registradas pertencem a este apelido e nao podem se misturar com as
    de outra pessoa na mesma avaliacao.
    """
    col_a, col_b = st.columns([8, 1], vertical_alignment="center")
    col_a.markdown(
        f'<div style="font-size:13px;color:{CORES["muted"]}">Identificado como '
        f'<strong style="color:{CORES["ink"]}">{html.escape(apelido)}</strong></div>',
        unsafe_allow_html=True,
    )
    if col_b.button(
        "Trocar",
        key="trocar_apelido",
        type="tertiary",
        disabled=bool(st.session_state.get("sessoes_concluidas")),
        help="Indisponivel depois de concluir um modulo nesta visita.",
    ):
        st.session_state.apelido = ""
        st.rerun()


def render() -> None:
    if st.session_state.pop("agradecer", False):
        st.toast("Obrigado por participar da pesquisa!")

    apelido = (st.session_state.get("apelido") or "").strip()
    if not apelido:
        # Unico dialogo desta tela; o de fim de modulo so abre na tela "jogo".
        dialogo_identificacao()
    else:
        _identificacao(apelido)

    titulo(
        "Jogo visualizador de algoritmos",
        eyebrow="prototipo · UNIDAVI",
        apoio="Responda desafios sobre ordenacao e busca e veja o algoritmo rodar "
              "passo a passo depois de cada resposta.",
    )

    st.markdown("### Como a pontuacao funciona")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="av-card">{etiqueta(f"teorica · peso 1 · {PONTOS_POR_PESO} pts", "cinza")}'
            f'<p style="color:{CORES["muted"]};font-size:13px;margin-top:8px">'
            "Perguntas de conceito, definicao e complexidade. Valem menos porque "
            "cobram reconhecimento.</p></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="av-card" style="background:{CORES["blue_soft"]};border-color:#C9DDF3">'
            f'{etiqueta(f"codigo em execucao · peso 2 · {2 * PONTOS_POR_PESO} pts")}'
            f'<p style="color:{CORES["ink2"]};font-size:13px;margin-top:8px">'
            "Perguntas em que voce preve o proximo passo do algoritmo. Valem o dobro "
            "porque exigem simular a execucao.</p></div>",
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown('<div class="av-eyebrow">Escolha uma trilha</div>', unsafe_allow_html=True)

    # Protecao apenas: sem apelido o dialogo de identificacao fica por cima.
    sem_apelido = not apelido

    for disciplina in repositorio.listar_disciplinas():
        conteudos = repositorio.listar_conteudos(disciplina["id_disciplina"])
        with st.expander(f"{disciplina['nome']} — {disciplina['descricao']}", expanded=True):
            for conteudo in conteudos:
                total = len(repositorio.listar_questoes(conteudo["id_conteudo"]))
                visuais = len(
                    repositorio.listar_questoes(conteudo["id_conteudo"], tipo="visual")
                )
                col_a, col_b = st.columns([4, 1])
                col_a.markdown(
                    f"**{conteudo['nome']}**  \n"
                    f"<span style='color:{CORES['muted']};font-size:13px'>"
                    f"{total} questoes · {visuais} com visualizacao</span>",
                    unsafe_allow_html=True,
                )
                if col_b.button(
                    "Comecar",
                    key=f"inicia_{conteudo['id_conteudo']}",
                    type="primary",
                    disabled=sem_apelido or total == 0,
                    use_container_width=True,
                ):
                    iniciar_rodada(conteudo["id_conteudo"])

    with st.expander("Escala de pesos adotada"):
        for peso, descricao in PESOS.items():
            st.markdown(f"- **Peso {peso}** ({peso * PONTOS_POR_PESO} pts) — {descricao}")
