"""Testes do pseudocodigo e do vinculo entre passos e linhas destacadas.

Executar com:  pytest testes/ -v

O destaque so ajuda o estudante se cada quadro apontar para a linha certa.
Estes testes garantem que todo passo gerado aponta para uma linha que
existe e que nenhuma linha destacavel ficou sem passo correspondente.
"""

import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algoritmos import MOTORES, PSEUDOCODIGO, indice_da_linha  # noqa: E402
from algoritmos.busca import busca_binaria  # noqa: E402
from algoritmos.ordenacao import bubble_sort  # noqa: E402
from componentes.visualizacao import html_pseudocodigo  # noqa: E402

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


def _entradas(chave):
    """Lista de (lista, alvo) cobrindo casos fixos e aleatorios."""
    random.seed(11)
    if MOTORES[chave]["precisa_alvo"]:
        entradas = []
        for _ in range(200):
            lista = sorted(random.sample(range(0, 80), random.randint(1, 10)))
            alvo = random.choice(lista + [999, -1])
            entradas.append((lista, alvo))
        entradas.append(([], 5))
        return entradas
    entradas = [(caso, None) for caso in CASOS]
    for _ in range(200):
        lista = [random.randint(-20, 99) for _ in range(random.randint(0, 9))]
        entradas.append((lista, None))
    return entradas


def _passos(chave, lista, alvo):
    motor = MOTORES[chave]
    return motor["fn"](lista, alvo) if motor["precisa_alvo"] else motor["fn"](lista)


def _rotulos(chave):
    return [rot for rot, _texto in PSEUDOCODIGO[chave] if rot is not None]


def test_todo_motor_tem_pseudocodigo():
    assert set(MOTORES) <= set(PSEUDOCODIGO)


@pytest.mark.parametrize("chave", list(PSEUDOCODIGO))
def test_rotulos_nao_se_repetem(chave):
    rotulos = _rotulos(chave)
    assert len(rotulos) == len(set(rotulos))


@pytest.mark.parametrize("chave", list(PSEUDOCODIGO))
def test_indentacao_em_multiplos_de_quatro(chave):
    for _rot, texto in PSEUDOCODIGO[chave]:
        recuo = len(texto) - len(texto.lstrip(" "))
        assert recuo % 4 == 0, f"recuo irregular em: {texto!r}"


@pytest.mark.parametrize("chave", list(MOTORES))
def test_todo_passo_aponta_para_linha_existente(chave):
    rotulos = set(_rotulos(chave))
    for lista, alvo in _entradas(chave):
        for passo in _passos(chave, lista, alvo):
            assert passo.linha is not None, f"passo sem linha: {passo.texto}"
            assert passo.linha in rotulos, f"rotulo desconhecido: {passo.linha}"


@pytest.mark.parametrize("chave", list(MOTORES))
def test_nenhuma_linha_destacavel_fica_orfa(chave):
    usados = set()
    for lista, alvo in _entradas(chave):
        usados.update(p.linha for p in _passos(chave, lista, alvo))
    orfas = set(_rotulos(chave)) - usados
    assert not orfas, f"linhas que nunca sao destacadas: {orfas}"


def test_bubble_troca_aponta_para_linha_de_troca():
    random.seed(7)
    for _ in range(100):
        lista = [random.randint(0, 50) for _ in range(random.randint(2, 9))]
        for passo in bubble_sort(lista):
            if passo.tipo == "troca":
                assert passo.linha == "troca"


def test_binaria_descarta_esquerda_e_encontra():
    passos = busca_binaria([2, 5, 8, 12, 16, 23, 38, 45], 23)
    assert passos[0].linha == "descarta_esq", "12 < 23: a metade esquerda sai"
    assert passos[-1].linha == "encontrou"


def test_indice_da_linha():
    assert indice_da_linha("bubble", "compara") == 2
    assert indice_da_linha("bubble", "inexistente") is None
    assert indice_da_linha("bubble", None) is None
    assert indice_da_linha("inexistente", "compara") is None


def test_html_pseudocodigo_escapa_e_destaca_uma_linha():
    resultado = html_pseudocodigo("selection", "compara")
    assert "&lt;" in resultado
    assert "a[j] < a" not in resultado
    assert resultado.count("av-linha ativa") == 1


def test_html_pseudocodigo_sem_rotulo_nao_destaca():
    """RN09: antes da resposta nenhuma linha fica destacada."""
    for chave in PSEUDOCODIGO:
        assert "av-linha ativa" not in html_pseudocodigo(chave, None)
