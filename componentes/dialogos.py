"""Pop-ups modais da visita: identificacao e fim de modulo.

Os dois usam dismissible=False: nao ha X, ESC nem clique fora; o dialogo
so fecha quando o estudante faz uma escolha (st.rerun() dentro dele).

O Streamlit permite apenas um dialogo por execucao do script. A exclusao
mutua vem das telas: o de identificacao so e chamado na tela "inicio" e o
de fim de modulo so na tela "jogo".
"""

import html

import streamlit as st

from servicos.identificacao import (MAX_CARACTERES_APELIDO, normalizar_apelido,
                                    validar_apelido)
from servicos.pontuacao import aproveitamento, resumir_visita

from .estilo import CORES
from .fluxo import conteudos_com_questoes, encerrar_visita, iniciar_rodada


def _apoio(texto: str) -> None:
    st.markdown(
        f'<p style="color:{CORES["muted"]};font-size:14px;margin-top:-4px">{texto}</p>',
        unsafe_allow_html=True,
    )


@st.dialog("Antes de comecar", dismissible=False)
def dialogo_identificacao() -> None:
    _apoio("A identificacao serve para registrar suas respostas na pesquisa. "
           "Nao precisa ser seu nome real.")

    # O input tem chave propria. A chave "apelido" nao pode pertencer a um
    # widget: quando o dialogo fecha, o widget deixa de ser desenhado e o
    # Streamlit apagaria o valor do session_state junto com ele.
    with st.form("form_identificacao", border=False):
        texto = st.text_input(
            "Como voce quer ser identificado?",
            key="apelido_input",
            placeholder="Ex.: aluno_01",
            max_chars=MAX_CARACTERES_APELIDO,
        )
        enviado = st.form_submit_button("Entrar", type="primary")

    if enviado:
        erros = validar_apelido(texto)
        if erros:
            st.error(erros[0])
        else:
            st.session_state.apelido = normalizar_apelido(texto)
            st.rerun()


@st.dialog("Modulo concluido", width="medium", dismissible=False)
def dialogo_fim_modulo() -> None:
    sessoes = st.session_state.get("sessoes_concluidas") or []
    if not sessoes:
        # Estado inconsistente (nao deveria ocorrer): fecha sem travar o aluno.
        st.session_state.fim_modulo_pendente = False
        st.session_state.tela = "inicio"
        st.rerun()
        return

    ultimo = sessoes[-1]
    st.markdown(f'<div class="av-eyebrow">{html.escape(ultimo["nome_conteudo"])}</div>',
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Pontuacao", f"{ultimo['pontos']} de {ultimo['maximo']}")
    col2.metric("Acertos", f"{ultimo['acertos']} de {ultimo['total']}")
    col3.metric("Aproveitamento",
                f"{aproveitamento(ultimo['pontos'], ultimo['maximo']):.0f}%")

    if len(sessoes) > 1:
        visita = resumir_visita(sessoes)
        st.caption(
            f"Total da visita: {len(sessoes)} modulos · "
            f"{visita['pontos']} de {visita['maximo']} pts · "
            f"{visita['acertos']} de {visita['total']} acertos · "
            f"{visita['aproveitamento']:.0f}% de aproveitamento"
        )

    st.divider()

    st.markdown("**Seguir para outro modulo**")
    opcoes = conteudos_com_questoes()
    rotulos = {o["id_conteudo"]: o["rotulo"] for o in opcoes}
    concluidos = {s["id_conteudo"] for s in sessoes}
    ids = list(rotulos)
    pendentes = [i for i in ids if i not in concluidos]
    escolha = st.selectbox(
        "Modulo",
        ids,
        index=ids.index(pendentes[0]) if pendentes else 0,
        format_func=lambda i: rotulos[i] + (" (concluido)" if i in concluidos else ""),
        label_visibility="collapsed",
        key="proximo_modulo",
    )
    if st.button("Ir para este modulo", disabled=escolha is None):
        iniciar_rodada(escolha)

    st.divider()

    st.markdown("**Ou encerre por aqui**")
    _apoio("Sua avaliacao do prototipo e a parte mais importante da pesquisa. "
           "Leva menos de um minuto.")
    if st.button("Encerrar e avaliar", type="primary"):
        encerrar_visita()
        st.rerun()
