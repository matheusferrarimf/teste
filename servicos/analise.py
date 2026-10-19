"""Analise das sessoes para a etapa de validacao da pesquisa.

As regras abaixo apenas SINALIZAM sessoes com indicios de resposta sem
atencao. A decisao de descartar continua sendo do pesquisador, e o
criterio precisa estar descrito na metodologia antes da coleta.
"""

LIMITE_SEG_POR_QUESTAO = 6
LIMITE_SEG_AVALIACAO = 12

CRITERIOS = [
    ("facilidade", "Facilidade de uso", "A interface foi facil de usar?"),
    ("visualizacao", "Clareza da visualizacao", "A animacao dos algoritmos ficou clara?"),
    ("entendimento", "Contribuicao para o entendimento",
     "A ferramenta ajudou voce a entender o conteudo?"),
    ("nivel", "Adequacao do nivel", "O nivel das perguntas foi adequado?"),
]


def sinalizar(sessao: dict) -> list:
    """Devolve a lista de motivos de alerta. Lista vazia = sessao valida."""
    motivos = []

    tempo_medio = sessao.get("tempo_medio") or 0
    if 0 < tempo_medio < LIMITE_SEG_POR_QUESTAO:
        motivos.append(f"Media de {tempo_medio:.0f}s por questao")

    tempo_av = sessao.get("tempo_preenchimento")
    if tempo_av is not None and tempo_av < LIMITE_SEG_AVALIACAO:
        motivos.append(f"Avaliacao respondida em {tempo_av}s")

    notas = [sessao.get(chave) for chave, _, _ in CRITERIOS]
    if all(n is not None for n in notas) and len(set(notas)) == 1:
        motivos.append("Mesma nota em todos os criterios")

    return motivos


def enriquecer(sessoes: list) -> list:
    for s in sessoes:
        s["motivos"] = sinalizar(s)
        s["valida"] = len(s["motivos"]) == 0
        s["aproveitamento"] = (
            s["acertos"] / s["total_questoes"] * 100 if s["total_questoes"] else 0
        )
    return sessoes


def medias_por_criterio(sessoes: list) -> dict:
    resultado = {}
    for chave, _, _ in CRITERIOS:
        valores = [s[chave] for s in sessoes if s.get(chave) is not None]
        resultado[chave] = sum(valores) / len(valores) if valores else 0.0
    return resultado


def resumo(sessoes: list) -> dict:
    if not sessoes:
        return {"sessoes": 0, "tempo_medio": 0, "aproveitamento": 0, "pontuacao": 0}
    return {
        "sessoes": len(sessoes),
        "tempo_medio": sum(s["tempo_medio"] for s in sessoes) / len(sessoes),
        "aproveitamento": sum(s["aproveitamento"] for s in sessoes) / len(sessoes),
        "pontuacao": sum(s["pontuacao_total"] for s in sessoes) / len(sessoes),
    }
