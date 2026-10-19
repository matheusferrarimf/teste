"""Tela inicial: identificacao do estudante e escolha do conteudo."""

import time

import streamlit as st

from componentes.estilo import CORES, titulo
from componentes.ui import etiqueta
from dados import repositorio
from servicos.controle_questao import montar_rodada
from servicos.pontuacao import PESOS, PONTOS_POR_PESO


def _iniciar_rodada(id_conteudo: int) -> None:
    questoes = montar_rodada(id_conteudo)
    if not questoes:
        st.warning("Este conteudo ainda nao possui questoes cadastradas.")
        return

    id_estudante = repositorio.obter_ou_criar_estudante(st.session_state.apelido)
    id_sessao = repositorio.criar_sessao(id_estudante, id_conteudo)

    st.session_state.rodada = {
        "id_sessao": id_sessao,
        "id_conteudo": id_conteudo,
        "questoes": questoes,
        "indice": 0,
        "pontos": 0,
        "acertos": 0,
        "tempos": [],
    }
    st.session_state.inicio_questao = time.time()
    st.session_state.respondida = False
    st.session_state.tela = "jogo"
    st.rerun()


def render() -> None:
    titulo(
        "Jogo visualizador de algoritmos",
        eyebrow="prototipo · UNIDAVI",
        apoio="Responda desafios sobre ordenacao e busca e veja o algoritmo rodar "
              "passo a passo depois de cada resposta.",
    )

    st.text_input(
        "Como voce quer ser identificado na pesquisa?",
        key="apelido",
        placeholder="Ex.: aluno_01",
        help="Nao e necessario usar seu nome real.",
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

    sem_apelido = not (st.session_state.get("apelido") or "").strip()
    if sem_apelido:
        st.info("Informe uma identificacao acima para comecar.")

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
                    _iniciar_rodada(conteudo["id_conteudo"])

    with st.expander("Escala de pesos adotada"):
        for peso, descricao in PESOS.items():
            st.markdown(f"- **Peso {peso}** ({peso * PONTOS_POR_PESO} pts) — {descricao}")
