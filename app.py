"""AlgoVis — prototipo de jogo para ensino de algoritmos.

Trabalho de Conclusao de Curso — Sistemas de Informacao — UNIDAVI.

Camada de apresentacao. Este arquivo apenas configura a pagina e decide
qual tela renderizar; toda a logica esta nos modulos servicos/, dados/ e
algoritmos/.
"""

import streamlit as st

from componentes import estilo
from dados.seed import popular_se_vazio
from paginas import avaliacao, cadastro, dashboard, inicio, jogo

st.set_page_config(
    page_title="AlgoVis — UNIDAVI",
    page_icon="▤",
    layout="wide",
    initial_sidebar_state="expanded",
)

estilo.aplicar()
popular_se_vazio()

# ── estado inicial da sessao ─────────────────────────────────────
PADROES = {
    "tela": "inicio",
    "rodada": None,
    "respondida": False,
    "resultado": None,
    "apelido": "",
    # resumo de cada modulo concluido nesta visita (ver componentes/fluxo.py)
    "sessoes_concluidas": [],
    "fim_modulo_pendente": False,
}
for chave, valor in PADROES.items():
    st.session_state.setdefault(chave, valor)

# ── navegacao ────────────────────────────────────────────────────
MENU = {
    "inicio": "Inicio",
    "cadastro": "Cadastrar perguntas",
    "dashboard": "Dashboard",
}

with st.sidebar:
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;padding:4px 0 14px">'
        f'<div style="width:32px;height:32px;border-radius:7px;background:'
        f'{estilo.CORES["blue"]};display:flex;align-items:center;justify-content:center;'
        f'color:#fff;font-weight:700">▤</div>'
        f'<div><div style="font-family:\'Space Grotesk\',sans-serif;font-weight:700;'
        f'font-size:15px;line-height:1.1">AlgoVis</div>'
        f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:9.5px;'
        f'letter-spacing:.1em;color:{estilo.CORES["gray"]}">UNIDAVI</div></div></div>',
        unsafe_allow_html=True,
    )

    # Cobre o jogo, o pop-up de fim de modulo (que abre na tela "jogo") e a avaliacao.
    em_rodada = (st.session_state.tela in ("jogo", "avaliacao")
                 or st.session_state.fim_modulo_pendente)
    for chave, rotulo in MENU.items():
        if st.button(
            rotulo,
            key=f"nav_{chave}",
            use_container_width=True,
            type="primary" if st.session_state.tela == chave else "secondary",
            disabled=em_rodada,
        ):
            st.session_state.rodada = None
            st.session_state.tela = chave
            st.rerun()

    if em_rodada:
        st.caption("Menu bloqueado durante a rodada para preservar o tempo de resposta.")

    st.divider()
    st.caption(
        "Prototipo academico. Os dados coletados sao usados apenas para a validacao "
        "descrita no trabalho."
    )

# ── roteamento ───────────────────────────────────────────────────
TELAS = {
    "inicio": inicio.render,
    "jogo": jogo.render,
    "cadastro": cadastro.render,
    "avaliacao": avaliacao.render,
    "dashboard": dashboard.render,
}

TELAS[st.session_state.tela]()
