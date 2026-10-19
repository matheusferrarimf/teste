"""Regras de negocio da rodada de perguntas."""

import random

from algoritmos import gerar_passos
from dados import repositorio

from .pontuacao import pontos_da_questao

QUESTOES_POR_RODADA = 6
MIN_ELEMENTOS_LISTA = 5
MAX_ELEMENTOS_LISTA = 10


def montar_rodada(id_conteudo: int, quantidade: int = QUESTOES_POR_RODADA) -> list:
    """Seleciona as questoes da sessao.

    Prioriza as questoes com visualizacao, porque sao o objeto central do
    prototipo, e completa a rodada com questoes teoricas. RN11: a ordem e
    embaralhada a cada nova sessao.
    """
    visuais = repositorio.listar_questoes(id_conteudo, tipo="visual")
    teoricas = repositorio.listar_questoes(id_conteudo, tipo="teorica")

    random.shuffle(visuais)
    random.shuffle(teoricas)

    selecionadas = visuais[:quantidade]
    faltam = quantidade - len(selecionadas)
    if faltam > 0:
        selecionadas += teoricas[:faltam]

    random.shuffle(selecionadas)
    return selecionadas


def validar_resposta(questao: dict, id_alternativa: int) -> dict:
    """RN01: existe exatamente uma alternativa correta por questao."""
    escolhida = next(
        (a for a in questao["alternativas"] if a["id_alternativa"] == id_alternativa), None
    )
    correta = bool(escolhida and escolhida["correta"])
    return {
        "correta": correta,
        "pontos": pontos_da_questao(questao["peso"]) if correta else 0,
        "explicacao": questao["explicacao"],
        "alternativa_correta": next(
            a["texto"] for a in questao["alternativas"] if a["correta"]
        ),
    }


def passos_da_questao(questao: dict) -> list:
    """RN09: os passos so sao gerados depois da resposta do estudante."""
    if questao["tipo_questao"] != "visual" or not questao.get("chave_algoritmo"):
        return []
    return gerar_passos(
        questao["chave_algoritmo"],
        questao["lista_inicial"],
        questao.get("valor_procurado"),
    )


def validar_lista(lista: list, chave_algoritmo: str) -> list:
    """Checagens de consistencia das questoes visuais (RN07 e RN08)."""
    erros = []
    if not MIN_ELEMENTOS_LISTA <= len(lista) <= MAX_ELEMENTOS_LISTA:
        erros.append(
            f"A lista deve ter entre {MIN_ELEMENTOS_LISTA} e {MAX_ELEMENTOS_LISTA} elementos."
        )
    if chave_algoritmo == "binaria" and lista != sorted(lista):
        erros.append("A busca binaria exige uma lista previamente ordenada.")
    return erros
