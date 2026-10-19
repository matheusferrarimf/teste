"""Estrutura comum aos geradores de passos dos algoritmos.

Cada algoritmo, em vez de apenas devolver o resultado final, devolve a
sequencia de estados intermediarios pelos quais a lista passou. E essa
sequencia que a camada de apresentacao transforma em animacao.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PassoExecucao:
    """Um quadro da animacao.

    lista        estado completo da lista neste momento
    foco         indices em destaque (os que estao sendo comparados/movidos)
    fixos        indices ja posicionados em definitivo
    descartados  indices fora do espaco de busca (usado na busca binaria)
    buraco       indices cujo conteudo ainda nao e valido

    O campo buraco existe por um motivo didatico. Algoritmos que deslocam
    elementos, como Insertion Sort e Merge Sort, deixam temporariamente
    valores repetidos na lista: a copia ja foi feita, mas a posicao de
    origem ainda nao foi sobrescrita. Sem marcar essas posicoes, o
    estudante veria um numero duplicado e concluiria que o algoritmo
    esta errado. Marcadas, elas comunicam exatamente o que sao: espaco
    aberto para receber o proximo valor.

    tipo         comparacao | troca | ok | fim
    texto        descricao em linguagem natural, exibida ao estudante
    chave        valor retirado da lista e mantido "na mao" (Insertion Sort)
    """

    lista: List[int]
    foco: List[int] = field(default_factory=list)
    fixos: List[int] = field(default_factory=list)
    descartados: List[int] = field(default_factory=list)
    buraco: List[int] = field(default_factory=list)
    tipo: str = "comparacao"
    texto: str = ""
    chave: int = None


def contar(passos: List[PassoExecucao]) -> dict:
    """Metricas simples usadas no feedback: quantas comparacoes e trocas."""
    return {
        "comparacoes": sum(1 for p in passos if p.tipo == "comparacao"),
        "trocas": sum(1 for p in passos if p.tipo == "troca"),
        "total": len(passos),
    }
