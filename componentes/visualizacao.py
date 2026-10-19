"""Renderizacao da lista e animacao passo a passo.

A animacao usa o padrao recomendado pelo Streamlit para conteudo que muda
ao longo do tempo: reserva-se uma area com st.empty() e o conteudo dessa
area e substituido a cada quadro.
"""

import time

import streamlit as st

from algoritmos.base import PassoExecucao

from .estilo import CORES

ALTURA = 200


def _cores_da_celula(indice: int, passo: PassoExecucao) -> tuple:
    """Devolve (fundo, borda, texto) conforme o papel do elemento no passo."""
    if indice in passo.buraco:
        return "#FFFFFF", CORES["gray"], "#C7D0DA"
    if indice in passo.descartados:
        return "#EEF2F7", "#E1E8F0", CORES["gray"]
    if indice in passo.foco:
        if passo.tipo == "troca":
            return CORES["blue_bright"], CORES["blue_deep"], "#FFFFFF"
        if passo.tipo == "fim":
            return CORES["ok"], CORES["ok"], "#FFFFFF"
        return "#F6C87A", CORES["amber"], "#4A2E00"
    if indice in passo.fixos:
        return CORES["ok_soft"], "#B9E3D2", CORES["ok"]
    return CORES["blue_soft"], "#C9DDF3", CORES["blue"]


def html_lista(passo: PassoExecucao) -> str:
    maximo = max(passo.lista) if passo.lista else 1
    barras, regua = [], []

    for i, valor in enumerate(passo.lista):
        fundo, borda, cor = _cores_da_celula(i, passo)
        altura = 44 + (valor / maximo) * (ALTURA - 60)
        extra = "transform:translateY(-6px);" if i in passo.foco else ""
        if i in passo.buraco:
            extra += "border-style:dashed;"
        barras.append(
            f'<div class="av-col"><div class="av-cel" style="height:{altura:.0f}px;'
            f'background:{fundo};border-color:{borda};color:{cor};{extra}">'
            f"{valor}</div></div>"
        )
        classe = "av-idx ativo" if i in passo.foco else "av-idx"
        regua.append(f'<div class="{classe}">{i}</div>')

    chave = ""
    if passo.chave is not None:
        chave = (
            f'<div style="text-align:center;margin-bottom:10px;font-family:'
            f"'IBM Plex Mono',monospace;font-size:12px;color:{CORES['muted']}\">"
            f"na mao: <strong style=\"color:{CORES['blue']}\">{passo.chave}</strong></div>"
        )

    legenda_buraco = ""
    if passo.buraco:
        legenda_buraco = (
            f'<div style="text-align:center;margin-top:6px;font-size:11.5px;'
            f'color:{CORES["gray"]}">Posicoes tracejadas ainda serao reescritas</div>'
        )

    return (
        f'<div class="av-trilho">{chave}'
        f'<div class="av-barras">{"".join(barras)}</div>'
        f'<div class="av-regua">{"".join(regua)}</div>'
        f"{legenda_buraco}</div>"
    )


def html_legenda(passo: PassoExecucao) -> str:
    if not passo.texto:
        return ""
    return (
        f'<div class="av-legenda"><div class="rot">{passo.tipo.upper()}</div>'
        f'<div class="txt">{passo.texto}</div></div>'
    )


def desenhar(passo: PassoExecucao, area=None) -> None:
    destino = area if area is not None else st
    destino.markdown(html_lista(passo) + html_legenda(passo), unsafe_allow_html=True)


def lista_estatica(lista: list, foco: list = None) -> None:
    """Estado inicial mostrado antes da resposta, sem revelar a execucao."""
    desenhar(PassoExecucao(lista=list(lista), foco=foco or [], tipo="comparacao", texto=""))


def animar(passos: list, area, intervalo: float = 0.75) -> None:
    """Executa a animacao completa dentro da area reservada."""
    barra = st.progress(0.0)
    for i, passo in enumerate(passos):
        desenhar(passo, area)
        barra.progress((i + 1) / len(passos))
        time.sleep(intervalo)
    barra.empty()


def controles_passo(passos: list, chave: str) -> None:
    """Navegacao manual, para quem prefere avancar no proprio ritmo."""
    estado = f"passo_{chave}"
    st.session_state.setdefault(estado, 0)
    atual = min(st.session_state[estado], len(passos) - 1)

    area = st.empty()
    desenhar(passos[atual], area)
    st.caption(f"Passo {atual + 1} de {len(passos)}")

    col1, col2, col3, col4 = st.columns(4)
    if col1.button("Voltar", key=f"volta_{chave}", disabled=atual == 0):
        st.session_state[estado] = atual - 1
        st.rerun()
    if col2.button("Avancar", key=f"avanca_{chave}", disabled=atual >= len(passos) - 1):
        st.session_state[estado] = atual + 1
        st.rerun()
    if col3.button("Executar tudo", key=f"exec_{chave}", type="primary"):
        animar(passos, area)
        st.session_state[estado] = len(passos) - 1
    if col4.button("Reiniciar", key=f"reset_{chave}"):
        st.session_state[estado] = 0
        st.rerun()
