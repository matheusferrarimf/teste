"""Transicoes de estado da visita do estudante.

Ficam aqui, e nao numa pagina, porque sao chamadas de mais de um lugar:
a tela inicial e o dialogo de fim de modulo iniciam rodadas, e a tela de
jogo e o dialogo encerram modulos e visitas.

Uma visita e o periodo entre a identificacao e o envio da avaliacao. Ela
pode ter varios modulos concluidos; cada um vira uma sessao no banco.
"""

import time

import streamlit as st

from dados import repositorio
from servicos.controle_questao import montar_rodada
from servicos.pontuacao import pontuacao_maxima


def iniciar_rodada(id_conteudo: int) -> None:
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
    st.session_state.resultado = None
    st.session_state.fim_modulo_pendente = False
    st.session_state.tela = "jogo"
    st.rerun()


def concluir_modulo() -> None:
    """Fecha a sessao no banco e guarda o resumo do modulo na visita."""
    rodada = st.session_state.rodada
    repositorio.finalizar_sessao(rodada["id_sessao"])

    conteudo = repositorio.buscar_conteudo(rodada["id_conteudo"]) or {}
    resumo = {
        "id_sessao": rodada["id_sessao"],
        "id_conteudo": rodada["id_conteudo"],
        "nome_conteudo": conteudo.get("nome", "Modulo"),
        "pontos": rodada["pontos"],
        "maximo": pontuacao_maxima(rodada["questoes"]),
        "acertos": rodada["acertos"],
        "total": len(rodada["questoes"]),
        "tempos": list(rodada["tempos"]),
    }
    # Reatribuir, em vez de usar append, evita alterar a lista padrao de app.py.
    st.session_state.sessoes_concluidas = [*st.session_state.sessoes_concluidas, resumo]

    # A navegacao manual guarda o passo atual por questao; se o modulo for
    # refeito, a animacao precisa recomecar do primeiro passo.
    for questao in rodada["questoes"]:
        st.session_state.pop(f"passo_q{questao['id_questao']}", None)

    st.session_state.rodada = None
    st.session_state.respondida = False
    st.session_state.resultado = None
    st.session_state.fim_modulo_pendente = True


def encerrar_visita() -> None:
    st.session_state.fim_modulo_pendente = False
    st.session_state.tela = "avaliacao"


def conteudos_com_questoes() -> list[dict]:
    """Conteudos que podem ser jogados, com o rotulo "Disciplina — Conteudo"."""
    opcoes = []
    for disciplina in repositorio.listar_disciplinas():
        for conteudo in repositorio.listar_conteudos(disciplina["id_disciplina"]):
            if repositorio.listar_questoes(conteudo["id_conteudo"]):
                opcoes.append({
                    "id_conteudo": conteudo["id_conteudo"],
                    "rotulo": f"{disciplina['nome']} — {conteudo['nome']}",
                })
    return opcoes
