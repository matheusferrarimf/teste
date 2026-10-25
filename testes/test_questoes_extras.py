"""Testes do banco de questoes da versao 2.

Executar com:  pytest testes/ -v

Duas preocupacoes:
1. O gabarito de cada questao visual e calculado a partir dos passos reais
   do gerador do algoritmo. Se alguem alterar um gerador ou uma questao e
   os dois deixarem de concordar, o teste falha.
2. A migracao precisa acrescentar as questoes num banco que ja esta em uso
   sem perder respostas coletadas, e nao pode ressuscitar questoes que o
   professor excluiu.
"""

import os
import sqlite3
import sys
import tempfile
import types
from collections import Counter
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

_st = types.ModuleType("streamlit")
_st.cache_resource = lambda f: (lambda _c={}: _c.setdefault("v", f()))
sys.modules.setdefault("streamlit", _st)

import dados.banco as banco  # noqa: E402

# Garante que nenhum teste toque no dados/algovis.db real.
banco.CAMINHO_BANCO = os.path.join(tempfile.mkdtemp(), "teste.db")

from algoritmos import contar, gerar_passos  # noqa: E402
from dados import repositorio, seed  # noqa: E402
from dados.questoes_extras import TEORICAS_V2, VISUAIS_V2  # noqa: E402
from servicos.controle_questao import validar_lista  # noqa: E402

CONTEUDOS = [nome for _, _, _, conteudos in seed.DISCIPLINAS for nome, _ in conteudos]


# ── utilitarios para ler os passos ───────────────────────────────
def _comparados(passos):
    """Valores efetivamente comparados numa busca, na ordem."""
    return [p.lista[p.foco[0]] for p in passos if p.foco]


def _passo(passos, inicio_do_texto):
    return next(p for p in passos if p.texto.startswith(inicio_do_texto))


# Para cada questao visual: funcao que recebe os passos e devolve o TEXTO
# da alternativa que deveria estar marcada como correta.
GABARITOS = {
    ("bubble", (5, 9, 3, 7, 2), None):
        lambda p: f"{_passo(p, 'Fim da passada 1').lista[-1]}, o maior valor da lista",
    ("linear", (6, 13, 2, 9, 4), 7):
        lambda p: f"Verifica os {len(_comparados(p))} elementos e conclui que o 7 nao esta na lista",
    ("linear", (9, 3, 7, 3, 5), 3):
        lambda p: f"Posicao {p[-1].foco[0]}, na primeira ocorrencia",
    ("linear", (14, 8, 21, 5, 17, 2, 11), 10):
        lambda p: str(len(_comparados(p))),
    ("bubble", (6, 2, 8, 4, 1), None):
        lambda p: str(_passo(p, "Fim da passada 1").lista),
    ("insertion", (3, 7, 4, 9, 2), None):
        lambda p: (f"O 7 e deslocado uma posicao para a direita e o 4 ocupa a posicao "
                   f"{_passo(p, 'Insere 4').foco[0]}"),
    ("selection", (1, 3, 5, 7, 9), None):
        lambda p: str(contar(p)["comparacoes"]),
    ("binaria", (3, 6, 9, 12, 15, 18, 21, 24, 27, 30), 30):
        lambda p: str(len(_comparados(p))),
    ("linear", (17, 8, 42, 23, 5, 31), 42):
        lambda p: f"Indice {p[-1].foco[0]}",
    ("insertion", (4, 1, 3, 9, 7), None):
        lambda p: str(_passo(p, "Insere 3").lista),
    ("binaria", (4, 9, 13, 18, 25, 31, 40), 9):
        lambda p: str([v for i, v in enumerate(p[1].lista) if i not in p[1].descartados]),
    ("binaria", (2, 6, 10, 14, 18, 22, 26, 30), 15):
        lambda p: ", ".join(str(v) for v in _comparados(p)),
    ("merge", (6, 2, 9, 4, 7, 1), None):
        lambda p: str(_passo(p, "Trecho das posicoes 0 a 1").lista[0:2]),
    ("selection", (5, 3, 8, 1, 6), None):
        lambda p: str(contar(p)["trocas"]),
}


# ── consistencia dos dados ───────────────────────────────────────
def test_cinco_teoricas_e_duas_visuais_por_conteudo():
    teoricas = Counter(q[0] for q in TEORICAS_V2)
    visuais = Counter(q[0] for q in VISUAIS_V2)
    for nome in CONTEUDOS:
        assert teoricas[nome] >= 5, nome
        assert visuais[nome] >= 2, nome


def test_conteudos_existem_na_carga_inicial():
    for q in TEORICAS_V2 + VISUAIS_V2:
        assert q[0] in CONTEUDOS


def test_enunciados_nao_se_repetem():
    todos = [q[1] for q in seed.TEORICAS + TEORICAS_V2] + \
            [q[4] for q in seed.VISUAIS + VISUAIS_V2]
    assert len(todos) == len(set(todos))


@pytest.mark.parametrize("q", TEORICAS_V2, ids=lambda q: q[1][:40])
def test_teoricas_respeitam_rn01_e_rn02(q):
    _, _, alts, correta, nivel, peso, explicacao = q
    assert 3 <= len(alts) <= 5
    assert 0 <= correta < len(alts)
    assert len(set(alts)) == len(alts), "alternativas repetidas"
    assert nivel in (1, 2, 3) and peso in (1, 2, 3)
    assert explicacao.strip()


@pytest.mark.parametrize("q", VISUAIS_V2, ids=lambda q: f"{q[1]}-{q[2]}")
def test_visuais_respeitam_rn07_e_rn08(q):
    _, chave, lista, alvo, _, alts, correta, _, _, _ = q
    assert validar_lista(lista, chave) == []
    assert 3 <= len(alts) <= 5 and 0 <= correta < len(alts)
    if chave in ("linear", "binaria"):
        assert alvo is not None


# ── gabaritos conferidos contra a execucao real ──────────────────
def test_toda_questao_visual_tem_gabarito_automatico():
    for _, chave, lista, alvo, *_ in VISUAIS_V2:
        assert (chave, tuple(lista), alvo) in GABARITOS


@pytest.mark.parametrize("q", VISUAIS_V2, ids=lambda q: f"{q[1]}-{q[2]}")
def test_gabarito_confere_com_o_algoritmo(q):
    _, chave, lista, alvo, enunciado, alts, correta, *_ = q
    passos = gerar_passos(chave, lista, alvo)
    esperado = GABARITOS[(chave, tuple(lista), alvo)](passos)
    assert alts[correta] == esperado, enunciado


# ── migracao de um banco que ja esta em uso ──────────────────────
@pytest.fixture
def banco_versao_1(monkeypatch, tmp_path):
    """Banco isolado no estado anterior a esta versao, com uma resposta coletada."""
    con = sqlite3.connect(tmp_path / "v1.db")
    con.row_factory = sqlite3.Row
    con.executescript(banco.ESQUEMA)
    monkeypatch.setattr(banco, "conexao", lambda: con)

    seed._carga_inicial()
    id_est = repositorio.obter_ou_criar_estudante("aluno_teste")
    id_sessao = repositorio.criar_sessao(id_est, repositorio.listar_conteudos()[0]["id_conteudo"])
    q = repositorio.listar_questoes()[0]
    repositorio.registrar_resposta(
        id_sessao, q["id_questao"], q["alternativas"][0]["id_alternativa"], True, 10, 12
    )
    yield con
    con.close()


def test_migracao_acrescenta_questoes_sem_perder_respostas(banco_versao_1):
    antes = len(repositorio.listar_questoes())
    assert antes == len(seed.TEORICAS) + len(seed.VISUAIS)

    seed.popular_se_vazio()

    depois = len(repositorio.listar_questoes())
    assert depois == antes + len(TEORICAS_V2) + len(VISUAIS_V2)
    assert banco.consultar_um("SELECT COUNT(*) AS n FROM resposta")["n"] == 1
    assert seed._versao_do_banco() == seed.VERSAO_ATUAL


def test_migracao_nao_duplica_ao_reabrir(banco_versao_1):
    seed.popular_se_vazio()
    total = len(repositorio.listar_questoes())
    seed.popular_se_vazio()
    assert len(repositorio.listar_questoes()) == total


def test_questao_excluida_pelo_professor_nao_volta(banco_versao_1):
    seed.popular_se_vazio()
    alvo = next(q for q in repositorio.listar_questoes(tipo="teorica")
                if q["enunciado"] == TEORICAS_V2[0][1])
    assert repositorio.excluir_questao(alvo["id_questao"])

    seed.popular_se_vazio()
    enunciados = [q["enunciado"] for q in repositorio.listar_questoes()]
    assert TEORICAS_V2[0][1] not in enunciados
