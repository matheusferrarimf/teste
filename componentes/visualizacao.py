"""Renderizacao da lista e animacao passo a passo.

A animacao usa o padrao recomendado pelo Streamlit para conteudo que muda
ao longo do tempo: reserva-se uma area com st.empty() e o conteudo dessa
area e substituido a cada quadro.

Quando a chave do algoritmo e informada, o pseudocodigo aparece ao lado da
lista, com a linha do passo atual destacada. Lista e pseudocodigo saem num
unico markdown(), para que o st.empty() troque os dois juntos a cada quadro.
"""

import html
import time

import streamlit as st

from algoritmos.base import PassoExecucao
from algoritmos.pseudocodigo import PSEUDOCODIGO

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


def html_pseudocodigo(chave_algoritmo: str, rotulo_ativo: str | None) -> str:
    """Bloco com o pseudocodigo; a linha com rotulo_ativo recebe destaque.

    Todo texto passa por html.escape(): o pseudocodigo tem < e > (como em
    a[j] < a[menor]), que o navegador leria como tags. O HTML sai numa linha
    so, porque uma linha em branco ou indentada encerraria o bloco HTML no
    markdown do Streamlit.
    """
    linhas = []
    for numero, (rotulo, texto) in enumerate(PSEUDOCODIGO.get(chave_algoritmo, []), start=1):
        ativa = rotulo is not None and rotulo == rotulo_ativo
        classe = "av-linha ativa" if ativa else "av-linha"
        linhas.append(
            f'<div class="{classe}"><span class="num">{numero}</span>'
            f'<span class="txt">{html.escape(texto)}</span></div>'
        )
    return (
        '<div class="av-codigo"><div class="av-eyebrow av-codigo-titulo">PSEUDOCODIGO</div>'
        f'<div class="av-codigo-linhas">{"".join(linhas)}</div></div>'
    )


def desenhar(passo: PassoExecucao, area=None, chave_algoritmo: str = None) -> None:
    destino = area if area is not None else st
    conteudo = html_lista(passo) + html_legenda(passo)
    if chave_algoritmo in PSEUDOCODIGO:
        conteudo = (
            f'<div class="av-visual"><div class="av-visual-lista">{conteudo}</div>'
            f"{html_pseudocodigo(chave_algoritmo, passo.linha)}</div>"
        )
    destino.markdown(conteudo, unsafe_allow_html=True)


def lista_estatica(lista: list, foco: list = None, chave_algoritmo: str = None) -> None:
    """Estado inicial mostrado antes da resposta, sem revelar a execucao.

    O pseudocodigo aparece, mas sem linha destacada (RN09): o passo
    montado aqui nao tem linha, logo nenhuma recebe a classe ativa.
    """
    desenhar(
        PassoExecucao(lista=list(lista), foco=foco or [], tipo="comparacao", texto="",
                      linha=None),
        chave_algoritmo=chave_algoritmo,
    )


def animar(passos: list, area, intervalo: float = 0.75, chave_algoritmo: str = None) -> None:
    """Executa a animacao completa dentro da area reservada."""
    barra = st.progress(0.0)
    for i, passo in enumerate(passos):
        desenhar(passo, area, chave_algoritmo)
        barra.progress((i + 1) / len(passos))
        time.sleep(intervalo)
    barra.empty()


def controles_passo(passos: list, chave: str, chave_algoritmo: str = None) -> None:
    """Navegacao manual, para quem prefere avancar no proprio ritmo."""
    estado = f"passo_{chave}"
    st.session_state.setdefault(estado, 0)
    atual = min(st.session_state[estado], len(passos) - 1)

    area = st.empty()
    desenhar(passos[atual], area, chave_algoritmo)
    st.caption(f"Passo {atual + 1} de {len(passos)}")

    col1, col2, col3, col4 = st.columns(4)
    if col1.button("Voltar", key=f"volta_{chave}", disabled=atual == 0):
        st.session_state[estado] = atual - 1
        st.rerun()
    if col2.button("Avancar", key=f"avanca_{chave}", disabled=atual >= len(passos) - 1):
        st.session_state[estado] = atual + 1
        st.rerun()
    if col3.button("Executar tudo", key=f"exec_{chave}", type="primary"):
        animar(passos, area, chave_algoritmo=chave_algoritmo)
        st.session_state[estado] = len(passos) - 1
    if col4.button("Reiniciar", key=f"reset_{chave}"):
        st.session_state[estado] = 0
        st.rerun()
