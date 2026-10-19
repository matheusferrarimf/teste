"""Testes das regras de negocio, da camada de dados e da analise.

Executar com:  pytest testes/ -v

O stub de streamlit permite testar dados/ e servicos/ sem subir a
aplicacao, o que evidencia na pratica o beneficio da separacao em
camadas descrita no capitulo de engenharia de software.
"""

import os
import sys
import tempfile
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# stub minimo: substitui o decorador de cache por um cache simples
_st = types.ModuleType("streamlit")
_st.cache_resource = lambda f: (lambda _c={}: _c.setdefault("v", f()))
sys.modules.setdefault("streamlit", _st)

import dados.banco as banco  # noqa: E402

banco.CAMINHO_BANCO = os.path.join(tempfile.mkdtemp(), "teste.db")

from dados import repositorio  # noqa: E402
from dados.seed import popular_se_vazio  # noqa: E402
from servicos.analise import (LIMITE_SEG_AVALIACAO,  # noqa: E402
                              LIMITE_SEG_POR_QUESTAO, medias_por_criterio,
                              sinalizar)
from servicos.controle_questao import (montar_rodada,  # noqa: E402
                                       passos_da_questao, validar_lista,
                                       validar_resposta)
from servicos.pontuacao import (liberou_proximo_nivel,  # noqa: E402
                                pontos_da_questao, pontuacao_maxima)


@pytest.fixture(scope="module", autouse=True)
def banco_populado():
    popular_se_vazio()
    return True


# ── carga inicial ────────────────────────────────────────────────
def test_seed_e_idempotente():
    antes = len(repositorio.listar_questoes())
    popular_se_vazio()
    assert len(repositorio.listar_questoes()) == antes


def test_existem_questoes_dos_dois_tipos():
    assert repositorio.listar_questoes(tipo="teorica")
    assert repositorio.listar_questoes(tipo="visual")


# ── regras de negocio do banco de questoes ───────────────────────
def test_rn01_uma_unica_alternativa_correta():
    for q in repositorio.listar_questoes():
        assert sum(a["correta"] for a in q["alternativas"]) == 1


def test_rn02_entre_tres_e_cinco_alternativas():
    for q in repositorio.listar_questoes():
        assert 3 <= len(q["alternativas"]) <= 5


def test_rn07_e_rn08_listas_das_questoes_visuais():
    for q in repositorio.listar_questoes(tipo="visual"):
        assert validar_lista(q["lista_inicial"], q["chave_algoritmo"]) == []


def test_toda_questao_visual_gera_passos():
    for q in repositorio.listar_questoes(tipo="visual"):
        assert passos_da_questao(q)


def test_questao_teorica_nao_gera_passos():
    q = repositorio.listar_questoes(tipo="teorica")[0]
    assert passos_da_questao(q) == []


# ── pontuacao ────────────────────────────────────────────────────
def test_pontos_seguem_o_peso():
    assert pontos_da_questao(1) == 10
    assert pontos_da_questao(2) == 20


def test_erro_nao_gera_pontuacao_negativa():
    q = repositorio.listar_questoes(tipo="teorica")[0]
    errada = next(a for a in q["alternativas"] if not a["correta"])
    assert validar_resposta(q, errada["id_alternativa"])["pontos"] == 0


def test_acerto_soma_peso_vezes_dez():
    q = repositorio.listar_questoes(tipo="visual")[0]
    certa = next(a for a in q["alternativas"] if a["correta"])
    resultado = validar_resposta(q, certa["id_alternativa"])
    assert resultado["correta"] is True
    assert resultado["pontos"] == q["peso"] * 10


def test_rn10_progressao_exige_setenta_por_cento():
    assert liberou_proximo_nivel(7, 10) is True
    assert liberou_proximo_nivel(6, 10) is False


# ── rodada ───────────────────────────────────────────────────────
def test_rodada_prioriza_questoes_visuais():
    cid = repositorio.listar_conteudos()[0]["id_conteudo"]
    rodada = montar_rodada(cid)
    visuais_disponiveis = repositorio.listar_questoes(cid, tipo="visual")
    if visuais_disponiveis:
        assert any(q["tipo_questao"] == "visual" for q in rodada)


def test_rodada_nao_repete_questoes():
    cid = repositorio.listar_conteudos()[1]["id_conteudo"]
    rodada = montar_rodada(cid)
    ids = [q["id_questao"] for q in rodada]
    assert len(ids) == len(set(ids))


def test_pontuacao_maxima_soma_os_pesos():
    cid = repositorio.listar_conteudos()[1]["id_conteudo"]
    rodada = montar_rodada(cid)
    assert pontuacao_maxima(rodada) == sum(q["peso"] * 10 for q in rodada)


# ── sessao completa ──────────────────────────────────────────────
def test_sessao_grava_pontuacao_correta():
    cid = repositorio.listar_conteudos()[1]["id_conteudo"]
    rodada = montar_rodada(cid)
    eid = repositorio.obter_ou_criar_estudante("teste_pontuacao")
    sid = repositorio.criar_sessao(eid, cid)

    esperado = 0
    for q in rodada:
        certa = next(a for a in q["alternativas"] if a["correta"])
        r = validar_resposta(q, certa["id_alternativa"])
        repositorio.registrar_resposta(sid, q["id_questao"], certa["id_alternativa"],
                                       r["correta"], r["pontos"], 20)
        esperado += r["pontos"]
    repositorio.finalizar_sessao(sid)

    sessao = next(s for s in repositorio.listar_sessoes_avaliadas() if s["id_sessao"] == sid)
    assert sessao["pontuacao_total"] == esperado
    assert sessao["erros"] == 0


def test_estudante_nao_e_duplicado():
    a = repositorio.obter_ou_criar_estudante("mesmo_apelido")
    b = repositorio.obter_ou_criar_estudante("mesmo_apelido")
    assert a == b


# ── cadastro ─────────────────────────────────────────────────────
def test_cadastro_e_exclusao_de_questao_teorica():
    cid = repositorio.listar_conteudos()[0]["id_conteudo"]
    antes = len(repositorio.listar_questoes(tipo="teorica"))

    qid = repositorio.inserir_questao_teorica(
        cid, "Pergunta de teste?", ["alfa", "beta", "gama"], 1, 2, 3, "Explicacao."
    )
    assert len(repositorio.listar_questoes(tipo="teorica")) == antes + 1

    nova = next(q for q in repositorio.listar_questoes(tipo="teorica") if q["id_questao"] == qid)
    assert nova["peso"] == 3
    assert next(a for a in nova["alternativas"] if a["correta"])["texto"] == "beta"

    repositorio.excluir_questao(qid)
    assert len(repositorio.listar_questoes(tipo="teorica")) == antes


def test_questao_visual_nao_pode_ser_excluida():
    visual = repositorio.listar_questoes(tipo="visual")[0]
    assert repositorio.excluir_questao(visual["id_questao"]) is False

    depois = next(
        (q for q in repositorio.listar_questoes(tipo="visual")
         if q["id_questao"] == visual["id_questao"]), None
    )
    assert depois is not None, "questoes fixas nao podem ser removidas"
    # a tentativa de exclusao nao pode deixar a questao sem alternativas
    assert len(depois["alternativas"]) == len(visual["alternativas"])
    assert sum(a["correta"] for a in depois["alternativas"]) == 1


# ── sinalizacao de respostas ─────────────────────────────────────
def test_sessao_atenta_nao_e_sinalizada():
    sessao = {"tempo_medio": 25, "tempo_preenchimento": 45,
              "facilidade": 4, "visualizacao": 5, "entendimento": 3, "nivel": 4}
    assert sinalizar(sessao) == []


def test_respostas_rapidas_sao_sinalizadas():
    sessao = {"tempo_medio": LIMITE_SEG_POR_QUESTAO - 1, "tempo_preenchimento": 45,
              "facilidade": 4, "visualizacao": 5, "entendimento": 3, "nivel": 4}
    assert len(sinalizar(sessao)) == 1


def test_avaliacao_apressada_e_sinalizada():
    sessao = {"tempo_medio": 30, "tempo_preenchimento": LIMITE_SEG_AVALIACAO - 1,
              "facilidade": 4, "visualizacao": 5, "entendimento": 3, "nivel": 4}
    assert len(sinalizar(sessao)) == 1


def test_notas_uniformes_sao_sinalizadas():
    sessao = {"tempo_medio": 30, "tempo_preenchimento": 45,
              "facilidade": 3, "visualizacao": 3, "entendimento": 3, "nivel": 3}
    assert "Mesma nota em todos os criterios" in sinalizar(sessao)


def test_sessao_sem_avaliacao_nao_quebra():
    sessao = {"tempo_medio": 30, "tempo_preenchimento": None,
              "facilidade": None, "visualizacao": None,
              "entendimento": None, "nivel": None}
    assert sinalizar(sessao) == []


def test_descarte_altera_as_medias():
    todas = [
        {"facilidade": 5, "visualizacao": 5, "entendimento": 5, "nivel": 5},
        {"facilidade": 1, "visualizacao": 1, "entendimento": 1, "nivel": 1},
    ]
    validas = todas[:1]
    assert medias_por_criterio(todas)["facilidade"] == 3.0
    assert medias_por_criterio(validas)["facilidade"] == 5.0
