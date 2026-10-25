"""Tela de questoes: enunciado, alternativas, feedback e visualizacao."""

import time

import streamlit as st

from algoritmos import MOTORES, contar
from componentes.dialogos import dialogo_fim_modulo
from componentes.estilo import CORES
from componentes.fluxo import concluir_modulo
from componentes.ui import badge_peso, etiqueta
from componentes.visualizacao import controles_passo, lista_estatica
from dados import repositorio
from servicos.controle_questao import passos_da_questao, validar_resposta


def _cabecalho(rodada: dict) -> None:
    col1, col2, col3 = st.columns([1, 3, 1])
    if col1.button("Sair", use_container_width=True):
        st.session_state.rodada = None
        st.session_state.tela = "inicio"
        st.rerun()

    total = len(rodada["questoes"])
    concluidas = rodada["indice"] + (1 if st.session_state.get("respondida") else 0)
    col2.progress(concluidas / total, text=f"Questao {rodada['indice'] + 1} de {total}")
    placar = etiqueta(f"{rodada['pontos']} pts")
    col3.markdown(
        f'<div style="text-align:right;padding-top:6px">{placar}</div>',
        unsafe_allow_html=True,
    )


def _confirmar(questao: dict, id_alternativa: int, rodada: dict) -> None:
    segundos = int(time.time() - st.session_state.inicio_questao)
    resultado = validar_resposta(questao, id_alternativa)

    repositorio.registrar_resposta(
        rodada["id_sessao"], questao["id_questao"], id_alternativa,
        resultado["correta"], resultado["pontos"], segundos,
    )

    rodada["pontos"] += resultado["pontos"]
    rodada["acertos"] += 1 if resultado["correta"] else 0
    rodada["tempos"].append(segundos)

    st.session_state.respondida = True
    st.session_state.resultado = resultado
    st.rerun()


def _proxima(rodada: dict) -> None:
    if rodada["indice"] + 1 >= len(rodada["questoes"]):
        concluir_modulo()
    else:
        rodada["indice"] += 1
        st.session_state.inicio_questao = time.time()
        st.session_state.respondida = False
        st.session_state.resultado = None
        st.session_state.pop(f"passo_q{rodada['questoes'][rodada['indice'] - 1]['id_questao']}", None)
    st.rerun()


def render() -> None:
    # Precisa vir antes da checagem de rodada: ao concluir o modulo a rodada
    # ja foi zerada, e sem esta ordem o aluno voltaria direto para o inicio.
    if st.session_state.get("fim_modulo_pendente"):
        st.markdown('<div class="av-eyebrow">Modulo concluido</div>',
                    unsafe_allow_html=True)
        dialogo_fim_modulo()
        return

    rodada = st.session_state.get("rodada")
    if not rodada:
        st.session_state.tela = "inicio"
        st.rerun()
        return

    questao = rodada["questoes"][rodada["indice"]]
    respondida = st.session_state.get("respondida", False)

    _cabecalho(rodada)
    st.markdown(badge_peso(questao), unsafe_allow_html=True)
    st.markdown(f"### {questao['enunciado']}")

    # ── area de visualizacao ────────────────────────────────────
    if questao["tipo_questao"] == "visual":
        motor = MOTORES[questao["chave_algoritmo"]]
        tags = etiqueta(motor["nome"]) + etiqueta(motor["complexidade"], "cinza")
        if questao.get("valor_procurado") is not None:
            tags += etiqueta(f"procurando {questao['valor_procurado']}", "ambar")
        st.markdown(tags, unsafe_allow_html=True)

        if not respondida:
            # RN09: a execucao so aparece depois da resposta, para nao entregar o gabarito
            foco = [0, 1] if questao["chave_algoritmo"] == "bubble" else []
            lista_estatica(questao["lista_inicial"], foco,
                           chave_algoritmo=questao["chave_algoritmo"])
            st.caption("A execucao completa aparece depois que voce responder.")
        else:
            passos = passos_da_questao(questao)
            controles_passo(passos, chave=f"q{questao['id_questao']}",
                            chave_algoritmo=questao["chave_algoritmo"])
            metricas = contar(passos)
            st.caption(
                f"{metricas['comparacoes']} comparacoes · {metricas['trocas']} movimentacoes "
                f"· {metricas['total']} passos no total"
            )

    # ── alternativas ────────────────────────────────────────────
    opcoes = {a["texto"]: a["id_alternativa"] for a in questao["alternativas"]}

    if not respondida:
        escolha = st.radio(
            "Escolha uma alternativa:",
            list(opcoes.keys()),
            index=None,
            key=f"radio_{questao['id_questao']}",
        )
        if st.button("Confirmar resposta", type="primary", disabled=escolha is None):
            _confirmar(questao, opcoes[escolha], rodada)
    else:
        resultado = st.session_state.resultado
        if resultado["correta"]:
            st.success(f"Correto — +{resultado['pontos']} pontos")
        else:
            st.error(f"Resposta incorreta. A alternativa correta era: {resultado['alternativa_correta']}")
        st.markdown(
            f'<div class="av-card" style="background:{CORES["blue_soft"]};'
            f'border-color:#C9DDF3">{resultado["explicacao"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        ultima = rodada["indice"] + 1 >= len(rodada["questoes"])
        if st.button("Concluir modulo" if ultima else "Proxima questao", type="primary"):
            _proxima(rodada)
