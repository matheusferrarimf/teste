"""Pseudocodigo de cada algoritmo, no estilo Portugol/VisuAlg.

Este modulo so fornece dados. Cada algoritmo e uma lista de linhas no
formato (rotulo, texto). O rotulo liga a linha aos passos gerados em
ordenacao.py e busca.py: cada PassoExecucao traz no campo linha o rotulo
da linha que o produziu, e a apresentacao destaca essa linha durante a
animacao. Linhas que nunca recebem destaque usam rotulo None.

A indentacao faz parte do texto (4 espacos por nivel).
"""

from typing import Optional

PSEUDOCODIGO: dict[str, list[tuple[str | None, str]]] = {
    "bubble": [
        (None,          "para i ← 0 ate n − 2 faca"),
        (None,          "    para j ← 0 ate n − 2 − i faca"),
        ("compara",     "        se a[j] > a[j + 1] entao"),
        ("troca",       "            trocar a[j] e a[j + 1]"),
        (None,          "        fim se"),
        ("fim_passada", "    fim para"),
        (None,          "fim para"),
        ("fim",         "retornar a"),
    ],
    "selection": [
        (None,           "para i ← 0 ate n − 2 faca"),
        ("assume_menor", "    menor ← i"),
        (None,           "    para j ← i + 1 ate n − 1 faca"),
        ("compara",      "        se a[j] < a[menor] entao"),
        ("novo_menor",   "            menor ← j"),
        (None,           "        fim se"),
        (None,           "    fim para"),
        (None,           "    se menor ≠ i entao"),
        ("troca",        "        trocar a[i] e a[menor]"),
        (None,           "    fim se"),
        (None,           "fim para"),
        ("fim",          "retornar a"),
    ],
    "insertion": [
        (None,      "para i ← 1 ate n − 1 faca"),
        ("retira",  "    chave ← a[i]"),
        (None,      "    j ← i − 1"),
        ("compara", "    enquanto j ≥ 0 e a[j] > chave faca"),
        ("desloca", "        a[j + 1] ← a[j]"),
        (None,      "        j ← j − 1"),
        (None,      "    fim enquanto"),
        ("insere",  "    a[j + 1] ← chave"),
        (None,      "fim para"),
        ("fim",     "retornar a"),
    ],
    "merge": [
        (None,        "procedimento MERGESORT(a, inicio, fim)"),
        (None,        "    se inicio < fim entao"),
        ("divide",    "        meio ← (inicio + fim) div 2"),
        (None,        "        MERGESORT(a, inicio, meio)"),
        (None,        "        MERGESORT(a, meio + 1, fim)"),
        (None,        "        INTERCALAR(a, inicio, meio, fim)"),
        (None,        "    fim se"),
        (None,        "fim procedimento"),
        (None,        "procedimento INTERCALAR(a, inicio, meio, fim)"),
        ("copia",     "    esq ← a[inicio..meio]; dir ← a[meio + 1..fim]"),
        (None,        "    enquanto houver elementos em esq e dir faca"),
        ("intercala", "        a[k] ← menor entre esq[i] e dir[j]"),
        (None,        "    fim enquanto"),
        ("resto_esq", "    copiar o restante de esq para a"),
        ("resto_dir", "    copiar o restante de dir para a"),
        ("trecho_ok", "    // trecho inicio..fim esta ordenado"),
        (None,        "fim procedimento"),
        ("fim",       "// lista completa ordenada"),
    ],
    "linear": [
        (None,            "para i ← 0 ate n − 1 faca"),
        ("compara",       "    se a[i] = alvo entao"),
        ("encontrou",     "        retornar i"),
        (None,            "    fim se"),
        (None,            "fim para"),
        ("nao_encontrou", "retornar −1"),
    ],
    "binaria": [
        (None,            "inicio ← 0; fim ← n − 1"),
        (None,            "enquanto inicio ≤ fim faca"),
        (None,            "    meio ← (inicio + fim) div 2"),
        (None,            "    se a[meio] = alvo entao"),
        ("encontrou",     "        retornar meio"),
        (None,            "    senao se a[meio] < alvo entao"),
        ("descarta_esq",  "        inicio ← meio + 1"),
        (None,            "    senao"),
        ("descarta_dir",  "        fim ← meio − 1"),
        (None,            "    fim se"),
        (None,            "fim enquanto"),
        ("nao_encontrou", "retornar −1"),
    ],
}


def indice_da_linha(chave_algoritmo: str, rotulo: Optional[str]) -> Optional[int]:
    """Posicao (a partir de 0) da linha com o rotulo dado, ou None se nao houver."""
    if rotulo is None:
        return None
    for indice, (rot, _texto) in enumerate(PSEUDOCODIGO.get(chave_algoritmo, [])):
        if rot == rotulo:
            return indice
    return None
