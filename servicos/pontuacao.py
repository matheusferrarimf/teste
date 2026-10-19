"""Regras de pontuacao do prototipo.

A pontuacao por peso e o elemento de gamificacao que diferencia perguntas
de reconhecimento (teoricas) de perguntas que exigem simular mentalmente a
execucao do algoritmo (visuais).
"""

PONTOS_POR_PESO = 10

PESOS = {
    1: "Reconhecimento de conceito",
    2: "Previsao do comportamento do algoritmo",
    3: "Analise e comparacao entre algoritmos",
}


def pontos_da_questao(peso: int) -> int:
    """RN05: acerto soma peso × 10; erro nao gera pontuacao negativa."""
    return peso * PONTOS_POR_PESO


def pontuacao_maxima(questoes: list) -> int:
    return sum(pontos_da_questao(q["peso"]) for q in questoes)


def aproveitamento(pontos: int, maximo: int) -> float:
    return (pontos / maximo * 100) if maximo else 0.0


def liberou_proximo_nivel(acertos: int, total: int, minimo: float = 0.70) -> bool:
    """RN10: avanco de nivel exige 70% de acertos."""
    return total > 0 and (acertos / total) >= minimo
