"""Algoritmos de busca instrumentados para visualizacao."""

from typing import List

from .base import PassoExecucao


def busca_linear(entrada: List[int], alvo: int) -> List[PassoExecucao]:
    a = list(entrada)
    passos: List[PassoExecucao] = []

    for i, valor in enumerate(a):
        if valor == alvo:
            passos.append(PassoExecucao(
                lista=list(a), foco=[i], descartados=list(range(i)), tipo="fim",
                texto=f"Encontrou {alvo} na posicao {i} — {i + 1} comparacoes",
            ))
            return passos
        passos.append(PassoExecucao(
            lista=list(a), foco=[i], descartados=list(range(i)),
            tipo="comparacao",
            texto=f"{valor} != {alvo} — avanca para a proxima posicao",
        ))

    passos.append(PassoExecucao(
        lista=list(a), descartados=list(range(len(a))), tipo="fim",
        texto=f"{alvo} nao esta na lista — {len(a)} comparacoes",
    ))
    return passos


def busca_binaria(entrada: List[int], alvo: int) -> List[PassoExecucao]:
    """Exige lista previamente ordenada (regra de negocio RN08)."""
    a = list(entrada)
    passos: List[PassoExecucao] = []
    inicio, fim = 0, len(a) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        descartados = list(range(0, inicio)) + list(range(fim + 1, len(a)))

        if a[meio] == alvo:
            passos.append(PassoExecucao(
                lista=list(a), foco=[meio], descartados=descartados, tipo="fim",
                texto=f"Meio = posicao {meio} ({a[meio]}) — encontrou {alvo}",
            ))
            return passos

        menor = a[meio] < alvo
        lado = "a esquerda" if menor else "a direita"
        passos.append(PassoExecucao(
            lista=list(a), foco=[meio], descartados=descartados,
            tipo="comparacao",
            texto=(f"Meio = posicao {meio} ({a[meio]}). "
                   f"{'Menor' if menor else 'Maior'} que {alvo} — descarta a metade {lado}"),
        ))
        if menor:
            inicio = meio + 1
        else:
            fim = meio - 1

    passos.append(PassoExecucao(
        lista=list(a), descartados=list(range(len(a))), tipo="fim",
        texto=f"{alvo} nao esta na lista",
    ))
    return passos
