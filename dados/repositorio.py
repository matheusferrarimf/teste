"""Camada de acesso a dados.

Nenhuma outra camada escreve SQL. Se o banco mudar, so este arquivo muda.
"""

import json
from datetime import datetime

from .banco import consultar, consultar_um, executar


def _agora() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ── disciplinas e conteudos ──────────────────────────────────────
def listar_disciplinas() -> list:
    return consultar("SELECT * FROM disciplina ORDER BY ordem, nome")


def listar_conteudos(id_disciplina=None) -> list:
    if id_disciplina is None:
        return consultar("SELECT * FROM conteudo ORDER BY ordem, nome")
    return consultar(
        "SELECT * FROM conteudo WHERE id_disciplina = ? ORDER BY ordem, nome",
        (id_disciplina,),
    )


def buscar_conteudo(id_conteudo):
    return consultar_um("SELECT * FROM conteudo WHERE id_conteudo = ?", (id_conteudo,))


# ── questoes ─────────────────────────────────────────────────────
def _montar_questao(linha: dict) -> dict:
    q = dict(linha)
    q["lista_inicial"] = json.loads(q["lista_inicial"]) if q["lista_inicial"] else None
    q["alternativas"] = consultar(
        "SELECT * FROM alternativa WHERE id_questao = ? ORDER BY ordem, id_alternativa",
        (q["id_questao"],),
    )
    return q


def listar_questoes(id_conteudo=None, tipo=None) -> list:
    sql = """
        SELECT q.*, a.chave AS chave_algoritmo, a.nome AS nome_algoritmo,
               a.complexidade_media, c.nome AS nome_conteudo
        FROM questao q
        LEFT JOIN algoritmo a ON a.id_algoritmo = q.id_algoritmo
        JOIN conteudo c ON c.id_conteudo = q.id_conteudo
        WHERE 1 = 1
    """
    parametros = []
    if id_conteudo is not None:
        sql += " AND q.id_conteudo = ?"
        parametros.append(id_conteudo)
    if tipo is not None:
        sql += " AND q.tipo_questao = ?"
        parametros.append(tipo)
    sql += " ORDER BY q.nivel_dificuldade, q.id_questao"
    return [_montar_questao(l) for l in consultar(sql, tuple(parametros))]


def inserir_questao_teorica(id_conteudo, enunciado, alternativas, indice_correta,
                            nivel, peso, explicacao) -> int:
    """alternativas: lista de textos. indice_correta: posicao na lista."""
    cur = executar(
        """INSERT INTO questao
           (id_conteudo, enunciado, tipo_questao, nivel_dificuldade, peso, explicacao, editavel)
           VALUES (?, ?, 'teorica', ?, ?, ?, 1)""",
        (id_conteudo, enunciado, nivel, peso, explicacao),
    )
    id_questao = cur.lastrowid
    for ordem, texto in enumerate(alternativas):
        executar(
            "INSERT INTO alternativa (id_questao, texto, correta, ordem) VALUES (?, ?, ?, ?)",
            (id_questao, texto, 1 if ordem == indice_correta else 0, ordem),
        )
    return id_questao


def excluir_questao(id_questao) -> bool:
    """Remove a questao e suas alternativas. Devolve False se for protegida.

    A verificacao de editavel precisa vir ANTES de tocar nas alternativas:
    do contrario, uma tentativa de excluir questao fixa apagaria suas
    alternativas e manteria a questao, deixando-a sem resposta possivel.
    """
    linha = consultar_um("SELECT editavel FROM questao WHERE id_questao = ?", (id_questao,))
    if not linha or not linha["editavel"]:
        return False
    executar("DELETE FROM alternativa WHERE id_questao = ?", (id_questao,))
    executar("DELETE FROM questao WHERE id_questao = ?", (id_questao,))
    return True


# ── sessoes, respostas e avaliacoes ──────────────────────────────
def obter_ou_criar_estudante(apelido: str) -> int:
    linha = consultar_um("SELECT id_estudante FROM estudante WHERE apelido = ?", (apelido,))
    if linha:
        return linha["id_estudante"]
    return executar(
        "INSERT INTO estudante (apelido, data_cadastro) VALUES (?, ?)",
        (apelido, _agora()),
    ).lastrowid


def criar_sessao(id_estudante, id_conteudo) -> int:
    return executar(
        "INSERT INTO sessao (id_estudante, id_conteudo, data_inicio) VALUES (?, ?, ?)",
        (id_estudante, id_conteudo, _agora()),
    ).lastrowid


def registrar_resposta(id_sessao, id_questao, id_alternativa, correta, pontos, segundos) -> None:
    executar(
        """INSERT INTO resposta
           (id_sessao, id_questao, id_alternativa, correta, pontos, tempo_resposta, data_hora)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (id_sessao, id_questao, id_alternativa, int(correta), pontos, segundos, _agora()),
    )


def finalizar_sessao(id_sessao) -> None:
    resumo = consultar_um(
        """SELECT COALESCE(SUM(pontos), 0)              AS pontos,
                  COALESCE(SUM(correta), 0)             AS acertos,
                  COALESCE(SUM(1 - correta), 0)         AS erros
           FROM resposta WHERE id_sessao = ?""",
        (id_sessao,),
    )
    executar(
        """UPDATE sessao SET data_fim = ?, pontuacao_total = ?, acertos = ?, erros = ?
           WHERE id_sessao = ?""",
        (_agora(), resumo["pontos"], resumo["acertos"], resumo["erros"], id_sessao),
    )


def salvar_avaliacao(id_sessao, notas: dict, comentario: str, segundos: int) -> None:
    executar(
        """INSERT OR REPLACE INTO avaliacao
           (id_sessao, facilidade, visualizacao, entendimento, nivel,
            comentario, tempo_preenchimento, data_hora)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (id_sessao, notas["facilidade"], notas["visualizacao"], notas["entendimento"],
         notas["nivel"], comentario, segundos, _agora()),
    )


def listar_sessoes_avaliadas() -> list:
    """Uma linha por sessao concluida, ja com as metricas do dashboard."""
    return consultar("""
        SELECT s.id_sessao, e.apelido, c.nome AS conteudo,
               s.data_inicio, s.pontuacao_total, s.acertos, s.erros,
               (s.acertos + s.erros) AS total_questoes,
               (SELECT COALESCE(AVG(r.tempo_resposta), 0) FROM resposta r
                 WHERE r.id_sessao = s.id_sessao) AS tempo_medio,
               (SELECT COALESCE(SUM(r.tempo_resposta), 0) FROM resposta r
                 WHERE r.id_sessao = s.id_sessao) AS tempo_total,
               av.facilidade, av.visualizacao, av.entendimento, av.nivel,
               av.comentario, av.tempo_preenchimento
        FROM sessao s
        JOIN estudante e ON e.id_estudante = s.id_estudante
        JOIN conteudo  c ON c.id_conteudo  = s.id_conteudo
        LEFT JOIN avaliacao av ON av.id_sessao = s.id_sessao
        WHERE s.data_fim IS NOT NULL
        ORDER BY s.data_inicio DESC
    """)


def estatisticas_por_questao() -> list:
    """Indice de erro por questao — util para revisar o banco de perguntas."""
    return consultar("""
        SELECT q.id_questao, q.enunciado, q.tipo_questao, q.peso,
               COUNT(r.id_resposta) AS respostas,
               COALESCE(SUM(r.correta), 0) AS acertos
        FROM questao q
        LEFT JOIN resposta r ON r.id_questao = q.id_questao
        GROUP BY q.id_questao
        HAVING respostas > 0
        ORDER BY (CAST(acertos AS REAL) / respostas) ASC
    """)
