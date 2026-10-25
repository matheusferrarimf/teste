"""Carga inicial do banco e migracoes do banco de questoes.

A carga inicial roda uma unica vez, num banco vazio. As versoes seguintes
do banco de questoes sao aplicadas por migracao (ver popular_se_vazio), o
que preserva as respostas e avaliacoes ja coletadas. As questoes
com visualizacao entram com editavel = 0, porque dependem do gerador de
passos de um algoritmo especifico e nao podem ser criadas pela tela de
cadastro.
"""

import json

from algoritmos import MOTORES

from .banco import consultar_um, executar
from .questoes_extras import TEORICAS_V2, VISUAIS_V2

# Versao do banco de questoes, gravada em PRAGMA user_version.
# 1 = carga original (TEORICAS e VISUAIS abaixo)
# 2 = questoes extras de dados/questoes_extras.py
VERSAO_ATUAL = 2

DISCIPLINAS = [
    ("Algoritmos I", "Conceitos iniciais e busca sequencial", 1, [
        ("Conceitos iniciais", 1),
        ("Busca sequencial", 1),
    ]),
    ("Algoritmos II", "Ordenacao e analise de complexidade", 2, [
        ("Ordenacao por comparacao", 2),
        ("Complexidade de algoritmos", 3),
    ]),
    ("Estrutura de Dados I", "Listas e operacoes de busca", 3, [
        ("Listas", 1),
        ("Busca binaria", 2),
    ]),
    ("Estrutura de Dados II", "Ordenacao aplicada a listas", 4, [
        ("Ordenacao aplicada a listas", 3),
    ]),
]

# (conteudo, enunciado, alternativas, indice_correta, nivel, peso, explicacao)
TEORICAS = [
    ("Conceitos iniciais",
     "O que caracteriza um algoritmo, segundo Cormen et al. (2012)?",
     ["Qualquer trecho de codigo escrito em Python",
      "Um procedimento que recebe entradas e produz saidas em passos bem definidos",
      "Uma estrutura usada para armazenar dados",
      "Um programa que roda no navegador"], 1, 1, 1,
     "Um algoritmo e um procedimento computacional bem definido que transforma uma ou mais "
     "entradas em uma ou mais saidas por meio de uma sequencia finita de passos."),

    ("Conceitos iniciais",
     "Qual estrutura permite repetir um bloco de comandos enquanto uma condicao for verdadeira?",
     ["Estrutura condicional", "Estrutura de repeticao", "Funcao", "Vetor"], 1, 1, 1,
     "Estruturas de repeticao, como while e for, executam um bloco varias vezes enquanto "
     "a condicao de parada nao for atingida."),

    ("Busca sequencial",
     "Qual e a complexidade da busca linear no pior caso?",
     ["O(1)", "O(log n)", "O(n)", "O(n²)"], 2, 1, 1,
     "No pior caso o elemento procurado esta na ultima posicao ou nao esta na lista, "
     "o que exige percorrer todos os n elementos."),

    ("Busca binaria",
     "Qual condicao e obrigatoria para aplicar a busca binaria?",
     ["A lista precisa estar ordenada", "A lista precisa ter tamanho par",
      "A lista precisa conter apenas numeros", "A lista precisa ter no maximo 10 elementos"],
     0, 1, 1,
     "A busca binaria descarta metade do espaco de busca comparando com o elemento central, "
     "o que so funciona se os dados estiverem previamente ordenados."),

    ("Ordenacao por comparacao",
     "Qual algoritmo de ordenacao utiliza a estrategia de divisao e conquista?",
     ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"], 3, 2, 1,
     "O Merge Sort divide a lista em partes menores, ordena cada parte e depois as combina, "
     "o que lhe garante complexidade O(n log n)."),

    ("Complexidade de algoritmos",
     "Um algoritmo O(n²) processa 100 elementos em 1 segundo. "
     "Aproximadamente quanto levaria com 200 elementos?",
     ["1 segundo", "2 segundos", "4 segundos", "100 segundos"], 2, 3, 2,
     "No crescimento quadratico, dobrar a entrada multiplica o tempo por quatro, pois (2n)² = 4n²."),

    ("Complexidade de algoritmos",
     "O que a notacao Big O descreve?",
     ["O tempo exato de execucao em segundos",
      "O crescimento do custo computacional conforme o tamanho da entrada",
      "A quantidade de linhas de codigo do algoritmo",
      "O consumo de energia do processador"], 1, 2, 1,
     "A notacao assintotica descreve como o custo cresce em funcao de n, desconsiderando "
     "detalhes de implementacao e caracteristicas do hardware."),

    ("Listas",
     "Em uma lista, o que identifica a posicao de cada elemento?",
     ["O valor armazenado", "O indice", "O tipo de dado", "O tamanho da lista"], 1, 1, 1,
     "O indice indica a posicao do elemento dentro da sequencia e e o que permite acessar "
     "diretamente qualquer item da lista."),

    ("Ordenacao aplicada a listas",
     "Por que o Bubble Sort costuma ser considerado ineficiente para listas grandes?",
     ["Porque consome muita memoria",
      "Porque realiza comparacoes repetidas entre elementos vizinhos, com custo O(n²)",
      "Porque nao funciona com numeros negativos",
      "Porque depende de a lista estar ordenada"], 1, 2, 1,
     "O Bubble Sort percorre a lista varias vezes comparando pares vizinhos, o que resulta "
     "em crescimento quadratico do numero de comparacoes."),
]

# (conteudo, algoritmo, lista, alvo, enunciado, alternativas, correta, nivel, peso, explicacao)
VISUAIS = [
    ("Ordenacao por comparacao", "bubble", [7, 3, 9, 1, 5], None,
     "O Bubble Sort vai comparar as posicoes 0 e 1 da lista abaixo. O que acontece em seguida?",
     ["Nada muda, pois 7 e 3 ja estao em ordem", "7 e 3 trocam de posicao",
      "7 vai direto para o fim da lista", "A lista e dividida ao meio"], 1, 1, 2,
     "No Bubble Sort a troca ocorre sempre que o elemento da esquerda e maior que o da direita. "
     "Como 7 > 3, os dois trocam de posicao."),

    ("Busca binaria", "binaria", [2, 5, 8, 12, 16, 23, 38, 45], 23,
     "A busca binaria vai procurar o valor 23 na lista ordenada abaixo. "
     "Qual e o primeiro elemento comparado?",
     ["2, o primeiro da lista", "45, o ultimo da lista",
      "12, o elemento do meio", "23, porque e o valor procurado"], 2, 2, 2,
     "A busca binaria sempre comeca pelo elemento central. Com 8 elementos, o indice do meio "
     "e 3, que contem o valor 12. Como 12 < 23, toda a metade a esquerda e descartada."),

    ("Ordenacao aplicada a listas", "selection", [4, 9, 2, 7, 1], None,
     "Ao final da primeira passada do Selection Sort, como fica a lista?",
     ["[1, 9, 2, 7, 4]", "[2, 4, 9, 7, 1]", "[4, 9, 2, 7, 1]", "[1, 2, 4, 7, 9]"], 0, 2, 2,
     "O Selection Sort percorre toda a lista procurando o menor valor e o coloca na primeira "
     "posicao. O menor e 1, que troca de lugar com o 4."),

    ("Busca sequencial", "linear", [11, 4, 8, 15, 3], 15,
     "Quantas comparacoes a busca linear precisa fazer para encontrar o valor 15?",
     ["1 comparacao", "3 comparacoes", "4 comparacoes", "5 comparacoes"], 2, 1, 2,
     "A busca linear verifica um elemento por vez, do inicio ao fim. O valor 15 esta na "
     "posicao 3, ou seja, e encontrado na quarta comparacao."),

    ("Listas", "insertion", [5, 2, 8, 1, 6], None,
     "No Insertion Sort, o que acontece com o valor 2 na primeira iteracao?",
     ["E comparado com 5 e deslocado para a posicao 0", "E removido da lista",
      "Troca de lugar com o 8", "Permanece na posicao 1"], 0, 3, 2,
     "O Insertion Sort retira o elemento e o insere na posicao correta da parte ja ordenada. "
     "Como 5 > 2, o 5 desloca-se para a direita e o 2 ocupa a posicao 0."),

    ("Ordenacao por comparacao", "merge", [8, 3, 5, 1, 9, 2], None,
     "No Merge Sort, o que acontece antes de qualquer comparacao entre elementos?",
     ["A lista e percorrida do inicio ao fim", "A lista e dividida ao meio, recursivamente",
      "O menor elemento e movido para a primeira posicao",
      "A lista e copiada para uma estrutura auxiliar ordenada"], 1, 3, 2,
     "O Merge Sort aplica divisao e conquista: primeiro divide a lista ate chegar a trechos "
     "de um elemento e so entao intercala os trechos de forma ordenada."),
]


def _id_conteudo(nome: str):
    linha = consultar_um("SELECT id_conteudo FROM conteudo WHERE nome = ?", (nome,))
    return linha["id_conteudo"] if linha else None


def _inserir_alternativas(id_questao, alternativas, correta):
    for ordem, texto in enumerate(alternativas):
        executar(
            "INSERT INTO alternativa (id_questao, texto, correta, ordem) VALUES (?, ?, ?, ?)",
            (id_questao, texto, 1 if ordem == correta else 0, ordem),
        )


def _ja_existe(id_conteudo, enunciado) -> bool:
    """Evita duplicar uma questao caso a migracao seja interrompida e reexecutada."""
    return consultar_um(
        "SELECT 1 AS ok FROM questao WHERE id_conteudo = ? AND enunciado = ?",
        (id_conteudo, enunciado),
    ) is not None


def _inserir_teoricas(questoes) -> None:
    for conteudo, enunciado, alts, correta, nivel, peso, explicacao in questoes:
        id_conteudo = _id_conteudo(conteudo)
        if _ja_existe(id_conteudo, enunciado):
            continue
        cur = executar(
            """INSERT INTO questao
               (id_conteudo, enunciado, tipo_questao, nivel_dificuldade, peso, explicacao, editavel)
               VALUES (?, ?, 'teorica', ?, ?, ?, 1)""",
            (id_conteudo, enunciado, nivel, peso, explicacao),
        )
        _inserir_alternativas(cur.lastrowid, alts, correta)


def _inserir_visuais(questoes) -> None:
    for (conteudo, chave_alg, lista, alvo, enunciado, alts,
         correta, nivel, peso, explicacao) in questoes:
        id_conteudo = _id_conteudo(conteudo)
        if _ja_existe(id_conteudo, enunciado):
            continue
        id_alg = consultar_um("SELECT id_algoritmo FROM algoritmo WHERE chave = ?", (chave_alg,))
        cur = executar(
            """INSERT INTO questao
               (id_conteudo, id_algoritmo, enunciado, tipo_questao, nivel_dificuldade,
                peso, lista_inicial, valor_procurado, explicacao, editavel)
               VALUES (?, ?, ?, 'visual', ?, ?, ?, ?, ?, 0)""",
            (id_conteudo, id_alg["id_algoritmo"], enunciado, nivel, peso,
             json.dumps(lista), alvo, explicacao),
        )
        _inserir_alternativas(cur.lastrowid, alts, correta)


def _carga_inicial() -> None:
    for nome, descricao, ordem, conteudos in DISCIPLINAS:
        cur = executar(
            "INSERT INTO disciplina (nome, descricao, ordem) VALUES (?, ?, ?)",
            (nome, descricao, ordem),
        )
        for i, (nome_c, nivel) in enumerate(conteudos):
            executar(
                "INSERT INTO conteudo (id_disciplina, nome, nivel, ordem) VALUES (?, ?, ?, ?)",
                (cur.lastrowid, nome_c, nivel, i),
            )

    for chave, motor in MOTORES.items():
        executar(
            """INSERT INTO algoritmo (chave, nome, tipo, complexidade_media)
               VALUES (?, ?, ?, ?)""",
            (chave, motor["nome"], motor["tipo"], motor["complexidade"]),
        )

    _inserir_teoricas(TEORICAS)
    _inserir_visuais(VISUAIS)


def _versao_do_banco() -> int:
    return consultar_um("PRAGMA user_version")["user_version"]


def popular_se_vazio() -> None:
    """Cria a carga inicial num banco vazio e aplica as migracoes pendentes.

    Bancos ja em uso (com respostas e avaliacoes coletadas) nao sao
    recriados: apenas recebem as questoes das versoes que ainda nao tem.
    A versao fica registrada em PRAGMA user_version, para que uma questao
    excluida pelo professor na tela de cadastro nao volte a cada abertura.
    """
    ja_tem = consultar_um("SELECT COUNT(*) AS n FROM disciplina")
    if not ja_tem or ja_tem["n"] == 0:
        _carga_inicial()

    versao = _versao_do_banco()
    if versao < 2:
        _inserir_teoricas(TEORICAS_V2)
        _inserir_visuais(VISUAIS_V2)
    if versao < VERSAO_ATUAL:
        executar(f"PRAGMA user_version = {VERSAO_ATUAL}")
