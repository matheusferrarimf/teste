"""Testes de unidade dos geradores de passos.

Executar com:  pytest testes/ -v

Estes testes sustentam a secao de testes de software do trabalho: eles
verificam nao apenas o resultado final, mas tambem a coerencia dos
estados intermediarios, que sao o que o estudante enxerga na animacao.
"""

import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algoritmos.busca import busca_binaria, busca_linear  # noqa: E402
from algoritmos.ordenacao import (bubble_sort, insertion_sort,  # noqa: E402
                                  merge_sort, selection_sort)

ORDENADORES = [bubble_sort, selection_sort, insertion_sort, merge_sort]
CASOS = [
    [],
    [1],
    [2, 1],
    [7, 3, 9, 1, 5],
    [1, 2, 3, 4, 5],          # ja ordenada
    [5, 4, 3, 2, 1],          # ordem inversa
    [4, 4, 4, 4],             # todos iguais
    [-3, 10, -3, 0, 7, -8],   # negativos e repetidos
]


@pytest.mark.parametrize("fn", ORDENADORES)
@pytest.mark.parametrize("entrada", CASOS)
def test_resultado_final_ordenado(fn, entrada):
    passos = fn(entrada)
    final = passos[-1].lista if passos else list(entrada)
    assert final == sorted(entrada)


@pytest.mark.parametrize("fn", ORDENADORES)
def test_entrada_nao_e_modificada(fn):
    entrada = [7, 3, 9, 1, 5]
    copia = list(entrada)
    fn(entrada)
    assert entrada == copia, "o gerador nao pode alterar a lista recebida"


@pytest.mark.parametrize("fn", ORDENADORES)
def test_estados_visiveis_nao_inventam_valores(fn):
    """Ignorando as posicoes marcadas como buraco, todo valor exibido ao
    estudante precisa existir na lista original."""
    random.seed(3)
    for _ in range(200):
        entrada = [random.randint(-20, 99) for _ in range(random.randint(0, 9))]
        for passo in fn(entrada):
            visiveis = [v for i, v in enumerate(passo.lista) if i not in passo.buraco]
            for valor in visiveis:
                assert valor in entrada


@pytest.mark.parametrize("fn", ORDENADORES)
def test_ultimo_passo_nao_tem_buraco(fn):
    """A lista final precisa estar integralmente valida."""
    passos = fn([7, 3, 9, 1, 5])
    assert passos[-1].buraco == []
    assert passos[-1].tipo == "fim"


@pytest.mark.parametrize("fn", ORDENADORES)
def test_indices_dentro_dos_limites(fn):
    entrada = [7, 3, 9, 1, 5]
    for passo in fn(entrada):
        for grupo in (passo.foco, passo.fixos, passo.descartados, passo.buraco):
            for i in grupo:
                assert 0 <= i < len(entrada)


@pytest.mark.parametrize("fn", ORDENADORES)
def test_todo_passo_tem_descricao(fn):
    for passo in fn([7, 3, 9, 1, 5]):
        assert passo.texto.strip(), "todo passo precisa de texto explicativo"


def test_busca_linear_encontra():
    passos = busca_linear([11, 4, 8, 15, 3], 15)
    assert "Encontrou" in passos[-1].texto
    assert passos[-1].foco == [3]
    assert len(passos) == 4, "deve fazer exatamente 4 comparacoes"


def test_busca_linear_nao_encontra():
    passos = busca_linear([11, 4, 8], 99)
    assert "nao esta na lista" in passos[-1].texto


def test_busca_binaria_comeca_pelo_meio():
    passos = busca_binaria([2, 5, 8, 12, 16, 23, 38, 45], 23)
    assert passos[0].foco == [3], "a primeira comparacao e com o elemento central"
    assert "encontrou" in passos[-1].texto


def test_busca_binaria_descarta_metade():
    passos = busca_binaria([2, 5, 8, 12, 16, 23, 38, 45], 23)
    assert len(passos[1].descartados) == 4, "apos o primeiro passo, metade sai"


def test_busca_binaria_e_logaritmica():
    """Numa lista de 64 elementos, no maximo 7 comparacoes."""
    lista = list(range(0, 128, 2))
    for alvo in lista:
        assert len(busca_binaria(lista, alvo)) <= 7


@pytest.mark.parametrize("busca", [busca_linear, busca_binaria])
def test_buscas_concordam(busca):
    random.seed(5)
    for _ in range(200):
        lista = sorted(random.sample(range(0, 80), random.randint(1, 10)))
        alvo = random.choice(lista + [999])
        passos = busca(lista, alvo)
        achou = "ncontrou" in passos[-1].texto
        assert achou == (alvo in lista)
