"""Testes da identificacao, do resumo da visita e dos pop-ups.

Executar com:  pytest testes/ -v

As regras (validar_apelido e resumir_visita) sao funcoes puras e sao
testadas sem Streamlit. Os pop-ups sao testados com o AppTest do proprio
Streamlit, rodando o app.py completo sobre um banco temporario.
"""

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

# Importa o Streamlit real antes que test_regras.py instale o stub dele.
try:
    import streamlit  # noqa: E402,F401
except ImportError:  # pragma: no cover
    pass

from servicos.identificacao import normalizar_apelido, validar_apelido  # noqa: E402
from servicos.pontuacao import resumir_visita  # noqa: E402


# ── validar_apelido ──────────────────────────────────────────────
@pytest.mark.parametrize("texto", ["", "   ", "ab", "a" * 31])
def test_apelido_invalido(texto):
    assert validar_apelido(texto)


@pytest.mark.parametrize("texto", ["abc", "aluno_01", "a" * 30])
def test_apelido_valido(texto):
    assert validar_apelido(texto) == []


def test_apelido_none_nao_quebra():
    assert validar_apelido(None)


def test_espacos_nas_pontas_sao_removidos():
    assert validar_apelido("  aluno_01  ") == []
    assert normalizar_apelido("  aluno_01  ") == "aluno_01"


def test_espacos_nao_contam_no_minimo():
    assert validar_apelido("  ab  "), "so 2 caracteres depois do strip"


# ── resumir_visita ───────────────────────────────────────────────
def _sessao(pontos, maximo, acertos, total, tempos):
    return {"id_sessao": 1, "id_conteudo": 1, "nome_conteudo": "X", "pontos": pontos,
            "maximo": maximo, "acertos": acertos, "total": total, "tempos": tempos}


def test_visita_vazia_nao_divide_por_zero():
    resumo = resumir_visita([])
    assert resumo == {"pontos": 0, "maximo": 0, "acertos": 0, "total": 0,
                      "tempo_medio": 0.0, "aproveitamento": 0.0}


def test_visita_com_um_modulo():
    resumo = resumir_visita([_sessao(60, 100, 4, 6, [10, 20, 30, 40, 50, 60])])
    assert resumo["pontos"] == 60
    assert resumo["maximo"] == 100
    assert resumo["acertos"] == 4
    assert resumo["total"] == 6
    assert resumo["tempo_medio"] == pytest.approx(35.0)
    assert resumo["aproveitamento"] == pytest.approx(60.0)


def test_visita_com_varios_modulos():
    resumo = resumir_visita([
        _sessao(60, 100, 4, 6, [10, 10]),
        _sessao(30, 50, 2, 3, [40]),
    ])
    assert resumo["pontos"] == 90
    assert resumo["maximo"] == 150
    assert resumo["acertos"] == 6
    assert resumo["total"] == 9
    # media de todas as questoes (60 / 3), nao a media das medias (25)
    assert resumo["tempo_medio"] == pytest.approx(20.0)
    assert resumo["aproveitamento"] == pytest.approx(60.0)


# ── pop-ups (AppTest) ────────────────────────────────────────────
@pytest.fixture
def app(tmp_path, monkeypatch):
    """app.py completo, com banco temporario para nao tocar no algovis.db."""
    try:
        from streamlit.testing.v1 import AppTest
    except ImportError:
        pytest.skip("streamlit real indisponivel (stub de test_regras ativo)")

    import dados.banco as banco
    if not hasattr(banco.conexao, "clear"):
        pytest.skip("dados.banco foi importado com o stub de streamlit")

    monkeypatch.setattr(banco, "CAMINHO_BANCO", str(tmp_path / "app.db"))
    banco.conexao.clear()
    yield AppTest.from_file(str(RAIZ / "app.py"), default_timeout=30)
    banco.conexao.clear()


def _botao(at, rotulo):
    return next(b for b in at.button if b.label == rotulo)


def test_dialogo_de_identificacao_abre_na_primeira_execucao(app):
    app.run()
    assert not app.exception
    assert app.text_input(key="apelido_input").placeholder == "Ex.: aluno_01"
    assert app.session_state.apelido == ""


def test_apelido_invalido_mantem_dialogo_aberto(app):
    app.run()
    app.text_input(key="apelido_input").input("ab")
    _botao(app, "Entrar").click().run()
    assert not app.exception
    assert app.error, "o erro aparece dentro do dialogo"
    assert app.text_input(key="apelido_input")
    assert app.session_state.apelido == ""


def test_apelido_valido_fecha_dialogo_e_sobrevive(app):
    app.run()
    app.text_input(key="apelido_input").input("  aluno_01  ")
    _botao(app, "Entrar").click().run()
    assert not app.exception
    assert app.session_state.apelido == "aluno_01"
    assert not [t for t in app.text_input if t.key == "apelido_input"]
    # um novo rerun nao pode apagar o apelido (a chave nao pertence a widget)
    app.run()
    assert app.session_state.apelido == "aluno_01"


def test_fim_de_modulo_leva_para_avaliacao(app):
    app.session_state["apelido"] = "aluno_01"
    app.session_state["tela"] = "jogo"
    app.session_state["fim_modulo_pendente"] = True
    app.session_state["sessoes_concluidas"] = [_sessao(60, 100, 4, 6, [10, 20])]
    app.run()
    assert not app.exception
    assert app.selectbox(key="proximo_modulo").options, "lista os modulos disponiveis"
    assert _botao(app, "Encerrar e avaliar").proto.type == "primary"

    _botao(app, "Encerrar e avaliar").click().run()
    assert not app.exception
    assert app.session_state.tela == "avaliacao"
    assert app.session_state.fim_modulo_pendente is False
