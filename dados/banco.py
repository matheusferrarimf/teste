"""Conexao com o banco e criacao do esquema.

O SQLite armazena todo o banco em um unico arquivo e dispensa servidor
dedicado, o que simplifica a distribuicao do prototipo.
"""

import os
import sqlite3

import streamlit as st

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), "algovis.db")

ESQUEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS disciplina (
    id_disciplina INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT    NOT NULL,
    descricao     TEXT,
    ordem         INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS conteudo (
    id_conteudo   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_disciplina INTEGER NOT NULL REFERENCES disciplina(id_disciplina),
    nome          TEXT    NOT NULL,
    nivel         INTEGER NOT NULL DEFAULT 1,
    ordem         INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS algoritmo (
    id_algoritmo       INTEGER PRIMARY KEY AUTOINCREMENT,
    chave              TEXT    NOT NULL UNIQUE,
    nome               TEXT    NOT NULL,
    tipo               TEXT    NOT NULL,
    complexidade_media TEXT
);

CREATE TABLE IF NOT EXISTS questao (
    id_questao        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_conteudo       INTEGER NOT NULL REFERENCES conteudo(id_conteudo),
    id_algoritmo      INTEGER REFERENCES algoritmo(id_algoritmo),
    enunciado         TEXT    NOT NULL,
    tipo_questao      TEXT    NOT NULL CHECK (tipo_questao IN ('teorica', 'visual')),
    nivel_dificuldade INTEGER NOT NULL DEFAULT 1,
    peso              INTEGER NOT NULL DEFAULT 1,
    lista_inicial     TEXT,
    valor_procurado   INTEGER,
    explicacao        TEXT    NOT NULL,
    editavel          INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS alternativa (
    id_alternativa INTEGER PRIMARY KEY AUTOINCREMENT,
    id_questao     INTEGER NOT NULL REFERENCES questao(id_questao) ON DELETE CASCADE,
    texto          TEXT    NOT NULL,
    correta        INTEGER NOT NULL DEFAULT 0,
    ordem          INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS estudante (
    id_estudante  INTEGER PRIMARY KEY AUTOINCREMENT,
    apelido       TEXT NOT NULL,
    data_cadastro TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessao (
    id_sessao       INTEGER PRIMARY KEY AUTOINCREMENT,
    id_estudante    INTEGER NOT NULL REFERENCES estudante(id_estudante),
    id_conteudo     INTEGER NOT NULL REFERENCES conteudo(id_conteudo),
    data_inicio     TEXT    NOT NULL,
    data_fim        TEXT,
    pontuacao_total INTEGER NOT NULL DEFAULT 0,
    acertos         INTEGER NOT NULL DEFAULT 0,
    erros           INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS resposta (
    id_resposta    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sessao      INTEGER NOT NULL REFERENCES sessao(id_sessao) ON DELETE CASCADE,
    id_questao     INTEGER NOT NULL REFERENCES questao(id_questao),
    id_alternativa INTEGER NOT NULL REFERENCES alternativa(id_alternativa),
    correta        INTEGER NOT NULL,
    pontos         INTEGER NOT NULL DEFAULT 0,
    tempo_resposta INTEGER,
    data_hora      TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS avaliacao (
    id_avaliacao        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sessao           INTEGER NOT NULL UNIQUE REFERENCES sessao(id_sessao) ON DELETE CASCADE,
    facilidade          INTEGER NOT NULL,
    visualizacao        INTEGER NOT NULL,
    entendimento        INTEGER NOT NULL,
    nivel               INTEGER NOT NULL,
    comentario          TEXT,
    tempo_preenchimento INTEGER,
    data_hora           TEXT    NOT NULL
);
"""


@st.cache_resource
def conexao() -> sqlite3.Connection:
    """Conexao unica reaproveitada entre os reruns do Streamlit."""
    con = sqlite3.connect(CAMINHO_BANCO, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.executescript(ESQUEMA)
    con.commit()
    return con


def executar(sql: str, parametros=()) -> sqlite3.Cursor:
    con = conexao()
    cur = con.execute(sql, parametros)
    con.commit()
    return cur


def consultar(sql: str, parametros=()) -> list:
    return [dict(linha) for linha in conexao().execute(sql, parametros).fetchall()]


def consultar_um(sql: str, parametros=()):
    linha = conexao().execute(sql, parametros).fetchone()
    return dict(linha) if linha else None
