"""Registro dos algoritmos disponiveis no prototipo.

Para acrescentar um algoritmo novo basta escrever o gerador de passos e
registra-lo em MOTORES. Nenhuma outra camada precisa ser alterada.
"""

from .base import PassoExecucao, contar
from .busca import busca_binaria, busca_linear
from .ordenacao import bubble_sort, insertion_sort, merge_sort, selection_sort
from .pseudocodigo import PSEUDOCODIGO, indice_da_linha

MOTORES = {
    "bubble": {
        "nome": "Bubble Sort", "tipo": "ordenacao",
        "complexidade": "O(n²)", "fn": bubble_sort, "precisa_alvo": False,
    },
    "selection": {
        "nome": "Selection Sort", "tipo": "ordenacao",
        "complexidade": "O(n²)", "fn": selection_sort, "precisa_alvo": False,
    },
    "insertion": {
        "nome": "Insertion Sort", "tipo": "ordenacao",
        "complexidade": "O(n²)", "fn": insertion_sort, "precisa_alvo": False,
    },
    "merge": {
        "nome": "Merge Sort", "tipo": "ordenacao",
        "complexidade": "O(n log n)", "fn": merge_sort, "precisa_alvo": False,
    },
    "linear": {
        "nome": "Busca linear", "tipo": "busca",
        "complexidade": "O(n)", "fn": busca_linear, "precisa_alvo": True,
    },
    "binaria": {
        "nome": "Busca binaria", "tipo": "busca",
        "complexidade": "O(log n)", "fn": busca_binaria, "precisa_alvo": True,
    },
}


def gerar_passos(chave, lista, alvo=None):
    """Ponto unico de entrada usado pela camada de servicos."""
    motor = MOTORES[chave]
    if motor["precisa_alvo"]:
        return motor["fn"](lista, alvo)
    return motor["fn"](lista)


__all__ = [
    "MOTORES", "gerar_passos", "PassoExecucao", "contar",
    "bubble_sort", "selection_sort", "insertion_sort", "merge_sort",
    "busca_linear", "busca_binaria",
    "PSEUDOCODIGO", "indice_da_linha",
]
