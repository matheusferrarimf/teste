"""Questoes acrescentadas na versao 2 do banco.

Cinco questoes teoricas e duas com visualizacao para cada conteudo. Ficam
separadas de seed.py para que a migracao possa inseri-las em bancos que ja
estao em uso, sem apagar respostas e avaliacoes coletadas.

Os gabaritos das questoes visuais sao conferidos contra os geradores de
passos em testes/test_questoes_extras.py.

Formato (o mesmo de seed.py):
  TEORICAS: (conteudo, enunciado, alternativas, indice_correta, nivel, peso, explicacao)
  VISUAIS:  (conteudo, algoritmo, lista, alvo, enunciado, alternativas,
             indice_correta, nivel, peso, explicacao)
"""

TEORICAS_V2 = [
    # ── Conceitos iniciais ───────────────────────────────────────
    ("Conceitos iniciais",
     "Qual das caracteristicas abaixo NAO e uma propriedade de um algoritmo?",
     ["Ter um numero finito de passos",
      "Ter passos bem definidos, sem ambiguidade",
      "Produzir ao menos uma saida",
      "Depender de uma linguagem de programacao especifica"], 3, 1, 1,
     "Um algoritmo descreve a solucao independentemente da linguagem. Ele pode ser escrito "
     "em pseudocodigo, fluxograma ou qualquer linguagem; finitude, passos bem definidos e "
     "producao de saida e que sao suas propriedades."),

    ("Conceitos iniciais",
     "Qual e a funcao de uma estrutura condicional (se / senao)?",
     ["Repetir um bloco de comandos varias vezes",
      "Escolher qual bloco de comandos executar de acordo com uma condicao",
      "Armazenar varios valores em uma unica variavel",
      "Encerrar a execucao do algoritmo"], 1, 1, 1,
     "A estrutura condicional avalia uma expressao logica e desvia o fluxo: se a condicao "
     "for verdadeira executa um bloco, senao executa outro (ou nenhum)."),

    ("Conceitos iniciais",
     "O que e uma variavel em um algoritmo?",
     ["Um espaco de memoria identificado por um nome, cujo valor pode mudar durante a execucao",
      "Um valor fixo que nunca pode ser alterado",
      "Um comando que exibe informacoes na tela",
      "Um tipo especial de estrutura de repeticao"], 0, 1, 1,
     "A variavel associa um nome a uma posicao de memoria. O valor guardado pode ser lido e "
     "substituido ao longo da execucao; um valor que nunca muda e chamado de constante."),

    ("Conceitos iniciais",
     "Considere o trecho: x ← 2; para i ← 1 ate 3 faca x ← x + 3; fim para. "
     "Qual e o valor de x ao final?",
     ["5", "8", "11", "14"], 2, 2, 2,
     "O laco executa 3 vezes (i = 1, 2 e 3). A cada volta x aumenta 3: 2 → 5 → 8 → 11."),

    ("Conceitos iniciais",
     "O que acontece com um laco enquanto cuja condicao nunca se torna falsa?",
     ["O laco executa uma unica vez",
      "O laco nao chega a executar",
      "O algoritmo para com erro de sintaxe",
      "O laco se repete indefinidamente (laco infinito)"], 3, 2, 1,
     "O enquanto so termina quando a condicao fica falsa. Se nada dentro do laco altera os "
     "valores que a condicao testa, ela nunca muda e o algoritmo nao termina, violando a "
     "propriedade de finitude."),

    # ── Busca sequencial ─────────────────────────────────────────
    ("Busca sequencial",
     "Qual e o melhor caso da busca linear?",
     ["O valor procurado esta no meio da lista",
      "O valor procurado esta na primeira posicao, exigindo uma unica comparacao",
      "O valor procurado nao esta na lista",
      "A lista esta ordenada"], 1, 1, 1,
     "A busca linear comeca pela posicao 0. Se o valor estiver ali, basta uma comparacao: "
     "esse e o melhor caso, O(1)."),

    ("Busca sequencial",
     "A busca linear exige que a lista esteja ordenada?",
     ["Sim, sempre",
      "Sim, quando a lista tem numeros negativos",
      "Nao, ela funciona com listas em qualquer ordem",
      "Apenas para listas com mais de 10 elementos"], 2, 1, 1,
     "A busca linear verifica um elemento por vez, sem fazer suposicoes sobre a ordem. Por "
     "isso funciona em qualquer lista, ao contrario da busca binaria."),

    ("Busca sequencial",
     "Em uma lista com 1000 elementos, quantas comparacoes a busca linear faz no pior caso?",
     ["1", "10", "500", "1000"], 3, 2, 2,
     "No pior caso o valor esta na ultima posicao ou nao esta na lista, e todos os n "
     "elementos sao verificados. Com n = 1000, sao 1000 comparacoes."),

    ("Busca sequencial",
     "O que a busca linear devolve quando o valor procurado nao esta na lista?",
     ["Um indicador de nao encontrado (por exemplo, -1), depois de verificar todos os elementos",
      "A posicao 0",
      "O ultimo elemento da lista",
      "O elemento mais proximo do valor procurado"], 0, 2, 1,
     "So e possivel concluir que o valor nao existe depois de verificar todas as posicoes. "
     "Entao a busca devolve um valor convencional que nao e indice valido, como -1."),

    ("Busca sequencial",
     "Supondo que o valor procurado esta na lista e tem a mesma chance de estar em qualquer "
     "posicao, quantas comparacoes a busca linear faz, em media, em uma lista de n elementos?",
     ["1", "Cerca de log n", "Cerca de n / 2", "n²"], 2, 3, 3,
     "Em media o valor e encontrado perto do meio da lista, o que da cerca de (n + 1) / 2 "
     "comparacoes. Mesmo assim o crescimento continua linear: O(n)."),

    # ── Ordenacao por comparacao ─────────────────────────────────
    ("Ordenacao por comparacao",
     "Qual algoritmo, a cada passada, procura o menor elemento da parte nao ordenada e o "
     "coloca na proxima posicao?",
     ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"], 1, 1, 1,
     "Essa e a estrategia do Selection Sort: selecionar o menor elemento restante e troca-lo "
     "com o primeiro elemento da parte ainda nao ordenada."),

    ("Ordenacao por comparacao",
     "No Bubble Sort, quais elementos sao comparados a cada passo?",
     ["Elementos vizinhos, nas posicoes j e j + 1",
      "O primeiro e o ultimo elemento da lista",
      "O elemento central e o valor procurado",
      "Todos os elementos ao mesmo tempo"], 0, 1, 1,
     "O Bubble Sort compara pares de vizinhos e troca os dois quando estao fora de ordem, "
     "fazendo os maiores valores 'subirem' para o fim da lista."),

    ("Ordenacao por comparacao",
     "Qual algoritmo funciona de forma parecida com organizar cartas de baralho na mao, "
     "inserindo cada nova carta na posicao correta entre as que ja estao ordenadas?",
     ["Merge Sort", "Selection Sort", "Insertion Sort", "Bubble Sort"], 2, 1, 1,
     "O Insertion Sort mantem uma parte ordenada no inicio da lista e insere cada novo "
     "elemento nela, deslocando para a direita os maiores."),

    ("Ordenacao por comparacao",
     "Apos a primeira passada completa do Bubble Sort em ordem crescente, o que se pode "
     "garantir?",
     ["O menor elemento esta na primeira posicao",
      "A lista ja esta ordenada",
      "Metade da lista esta ordenada",
      "O maior elemento esta na ultima posicao"], 3, 2, 2,
     "Ao comparar vizinhos da esquerda para a direita, o maior valor e levado ate o fim na "
     "primeira passada. Nada se garante sobre o menor, que se move apenas uma posicao por "
     "passada."),

    ("Ordenacao por comparacao",
     "Por que o Merge Sort usa memoria adicional, ao contrario de Bubble, Selection e "
     "Insertion Sort?",
     ["Porque precisa guardar a lista original para comparar no final",
      "Porque, ao intercalar, copia as duas metades para listas auxiliares",
      "Porque ordena a lista duas vezes",
      "Porque nao funciona com listas de numeros inteiros"], 1, 3, 3,
     "Na etapa de intercalacao, as metades sao copiadas para listas auxiliares e depois "
     "devolvidas em ordem. Isso exige espaco proporcional a n, enquanto os outros tres "
     "ordenam trocando elementos dentro da propria lista."),

    # ── Complexidade de algoritmos ───────────────────────────────
    ("Complexidade de algoritmos",
     "Qual e a complexidade do Merge Sort no pior caso?",
     ["O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"], 1, 2, 1,
     "O Merge Sort divide a lista em log n niveis e, em cada nivel, intercala n elementos. "
     "O custo e O(n log n) em qualquer caso, inclusive no pior."),

    ("Complexidade de algoritmos",
     "Qual destas ordens de crescimento e a mais eficiente para entradas grandes?",
     ["O(n²)", "O(n)", "O(log n)", "O(n log n)"], 2, 2, 1,
     "Em ordem do mais eficiente para o menos eficiente: O(log n), O(n), O(n log n), O(n²). "
     "O logaritmo cresce muito devagar: para n = 1 milhao, log₂ n e cerca de 20."),

    ("Complexidade de algoritmos",
     "Uma lista ordenada tem 1024 elementos. No pior caso, quantas comparacoes a busca "
     "binaria precisa, aproximadamente?",
     ["Cerca de 10", "Cerca de 100", "512", "1024"], 0, 3, 3,
     "Cada comparacao descarta metade da lista: 1024 → 512 → 256 → ... → 1. Sao log₂ 1024 = 10 "
     "divisoes, entao o pior caso fica em torno de 10 comparacoes (no maximo 11)."),

    ("Complexidade de algoritmos",
     "Qual e a complexidade do Insertion Sort no melhor caso, quando a lista ja esta "
     "ordenada?",
     ["O(1)", "O(log n)", "O(n²)", "O(n)"], 3, 3, 3,
     "Com a lista ordenada, cada elemento e comparado apenas com o anterior e ja esta no "
     "lugar certo, sem deslocamentos. Sao n - 1 comparacoes, ou seja, O(n)."),

    ("Complexidade de algoritmos",
     "O que mede a complexidade de espaco de um algoritmo?",
     ["O tamanho do arquivo do codigo-fonte",
      "O tempo de execucao em segundos",
      "A quantidade de memoria que o algoritmo usa conforme a entrada cresce",
      "O numero de linhas do pseudocodigo"], 2, 2, 1,
     "Enquanto a complexidade de tempo conta operacoes, a de espaco conta a memoria "
     "necessaria em funcao do tamanho da entrada. O Merge Sort, por exemplo, usa O(n) de "
     "memoria auxiliar."),

    # ── Listas ───────────────────────────────────────────────────
    ("Listas",
     "Qual e o custo de acessar um elemento de um vetor pelo seu indice?",
     ["O(1), acesso direto", "O(n)", "O(log n)", "O(n²)"], 0, 2, 1,
     "Em um vetor os elementos ficam em posicoes contiguas de memoria, entao o endereco de "
     "qualquer indice e calculado diretamente, sem percorrer a lista."),

    ("Listas",
     "Em Python, qual comando insere o valor x no final da lista?",
     ["lista.pop()", "lista.remove(x)", "lista.append(x)", "lista.sort()"], 2, 1, 1,
     "append acrescenta x depois do ultimo elemento. pop remove o ultimo, remove apaga a "
     "primeira ocorrencia de x e sort ordena a lista."),

    ("Listas",
     "O que acontece com os demais elementos quando um valor e inserido no inicio de uma "
     "lista sequencial (vetor)?",
     ["Nada, o novo valor substitui o primeiro",
      "Todos sao deslocados uma posicao para a direita",
      "A lista e ordenada automaticamente",
      "O ultimo elemento e descartado"], 1, 2, 2,
     "Para abrir espaco na posicao 0, cada elemento precisa ir uma posicao para a direita. "
     "E o mesmo deslocamento que o Insertion Sort faz ao inserir um valor na parte "
     "ordenada."),

    ("Listas",
     "Qual e a diferenca entre uma pilha e uma fila?",
     ["Na pilha o primeiro a entrar e o primeiro a sair; na fila o ultimo a entrar e o primeiro a sair",
      "Pilhas guardam apenas numeros e filas apenas textos",
      "Nao ha diferenca, sao nomes diferentes para a mesma estrutura",
      "Na pilha o ultimo a entrar e o primeiro a sair; na fila o primeiro a entrar e o primeiro a sair"],
     3, 1, 1,
     "A pilha segue a logica LIFO (como uma pilha de pratos) e a fila segue a logica FIFO "
     "(como uma fila de banco)."),

    ("Listas",
     "Dada a lista [10, 20, 30, 40, 50], qual valor esta em lista[2]?",
     ["20", "30", "40", "2"], 1, 1, 1,
     "Os indices comecam em 0: lista[0] = 10, lista[1] = 20 e lista[2] = 30."),

    # ── Busca binaria ────────────────────────────────────────────
    ("Busca binaria",
     "Na busca binaria, se o elemento do meio e menor que o valor procurado, o que acontece?",
     ["A busca continua na metade da direita",
      "A busca continua na metade da esquerda",
      "A busca recomeca do primeiro elemento",
      "A busca termina sem encontrar o valor"], 0, 1, 1,
     "Como a lista esta ordenada, tudo o que esta a esquerda do meio tambem e menor que o "
     "valor procurado. Essa metade e descartada e a busca segue na direita."),

    ("Busca binaria",
     "Qual e a complexidade da busca binaria?",
     ["O(1)", "O(n)", "O(log n)", "O(n log n)"], 2, 1, 1,
     "A cada comparacao o espaco de busca cai pela metade, entao o numero de comparacoes "
     "cresce com o logaritmo de n."),

    ("Busca binaria",
     "Como o prototipo calcula o indice do meio na busca binaria?",
     ["(inicio + fim) / 2, mantendo as casas decimais",
      "fim - inicio",
      "(inicio + fim) // 2, com divisao inteira",
      "Sempre o indice n / 2 da lista original"], 2, 2, 1,
     "O meio e a media entre inicio e fim com divisao inteira, pois indice precisa ser "
     "inteiro. Ele e recalculado a cada passo, sobre o trecho que ainda resta."),

    ("Busca binaria",
     "Quando a busca binaria conclui que o valor nao esta na lista?",
     ["Quando o elemento do meio e maior que o valor procurado",
      "Quando inicio fica maior que fim, ou seja, o espaco de busca ficou vazio",
      "Depois de exatamente log n comparacoes",
      "Quando chega ao ultimo elemento da lista"], 1, 2, 2,
     "Enquanto inicio ≤ fim ainda existe trecho a examinar. Quando inicio passa de fim, "
     "nao sobrou nenhuma posicao onde o valor poderia estar."),

    ("Busca binaria",
     "Ao dobrar o tamanho de uma lista ordenada, quantas comparacoes a mais a busca binaria "
     "faz no pior caso?",
     ["O dobro de comparacoes", "Quatro vezes mais", "Apenas uma a mais", "Nenhuma"],
     2, 3, 3,
     "A primeira comparacao da lista dobrada descarta metade dela, voltando ao tamanho "
     "original. Por isso o custo aumenta em apenas uma comparacao: e o comportamento "
     "logaritmico."),

    # ── Ordenacao aplicada a listas ──────────────────────────────
    ("Ordenacao aplicada a listas",
     "Considerando apenas o tempo de execucao, qual algoritmo e mais indicado para ordenar "
     "uma lista muito grande?",
     ["Bubble Sort", "Selection Sort", "Merge Sort", "Insertion Sort"], 2, 2, 2,
     "Merge Sort e O(n log n) em qualquer caso. Os outros tres sao O(n²) no pior caso, o "
     "que se torna proibitivo quando n e grande."),

    ("Ordenacao aplicada a listas",
     "O que significa dizer que um algoritmo de ordenacao e estavel?",
     ["Que ele nunca entra em laco infinito",
      "Que ele leva sempre o mesmo tempo",
      "Que ele usa sempre a mesma quantidade de memoria",
      "Que elementos com valores iguais mantem a ordem relativa que tinham antes"], 3, 2, 1,
     "Estabilidade importa quando se ordena por um criterio e se quer preservar uma ordem "
     "anterior, por exemplo ordenar alunos por nota mantendo a ordem alfabetica entre "
     "empatados."),

    ("Ordenacao aplicada a listas",
     "Na implementacao classica, qual destes algoritmos NAO e estavel?",
     ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"], 1, 3, 3,
     "O Selection Sort troca o menor elemento com uma posicao distante, o que pode passar um "
     "elemento por cima de outro de mesmo valor. Bubble e Insertion so movem vizinhos, e o "
     "Merge Sort preserva a ordem ao intercalar com <=."),

    ("Ordenacao aplicada a listas",
     "Para uma lista que ja esta quase ordenada, qual algoritmo simples tende a ser o mais "
     "rapido?",
     ["Insertion Sort", "Selection Sort", "Bubble Sort", "Todos levam o mesmo tempo"],
     0, 3, 3,
     "No Insertion Sort cada elemento so e deslocado enquanto houver maiores a sua esquerda. "
     "Com poucos elementos fora do lugar, sao poucos deslocamentos e o custo se aproxima de "
     "O(n). O Selection Sort, por outro lado, faz todas as comparacoes sempre."),

    ("Ordenacao aplicada a listas",
     "No maximo, quantas passadas o Bubble Sort precisa para ordenar uma lista de n "
     "elementos?",
     ["n", "n - 1", "n / 2", "log n"], 1, 2, 2,
     "Cada passada coloca um elemento na posicao final. Depois de n - 1 passadas, o "
     "elemento que sobrou so pode estar no lugar certo."),
]


VISUAIS_V2 = [
    # ── Conceitos iniciais ───────────────────────────────────────
    ("Conceitos iniciais", "bubble", [5, 9, 3, 7, 2], None,
     "O Bubble Sort percorre a lista comparando vizinhos e trocando quando o da esquerda e "
     "maior. Ao final da primeira passada, qual valor ocupa a ultima posicao?",
     ["2, que ja estava la", "7", "9, o maior valor da lista", "5, o primeiro valor da lista"],
     2, 1, 2,
     "O 9 e levado para a direita a cada comparacao em que e maior que o vizinho "
     "(9 > 3, 9 > 7, 9 > 2) ate chegar ao fim. A repeticao das comparacoes faz o maior "
     "valor terminar na ultima posicao."),

    ("Conceitos iniciais", "linear", [6, 13, 2, 9, 4], 7,
     "A busca linear vai procurar o valor 7 na lista abaixo. O que acontece?",
     ["Encontra o 7 na posicao 2",
      "Para no meio da lista",
      "Compara apenas o primeiro e o ultimo elemento",
      "Verifica os 5 elementos e conclui que o 7 nao esta na lista"], 3, 1, 2,
     "O laco compara cada elemento com 7. Como nenhum e igual, a repeticao so termina depois "
     "da ultima posicao, e o algoritmo informa que o valor nao foi encontrado."),

    # ── Busca sequencial ─────────────────────────────────────────
    ("Busca sequencial", "linear", [9, 3, 7, 3, 5], 3,
     "O valor 3 aparece duas vezes na lista abaixo. Em qual posicao a busca linear para?",
     ["Posicao 1, na primeira ocorrencia",
      "Posicao 3, na ultima ocorrencia",
      "Percorre toda a lista e devolve as duas posicoes",
      "Posicao 0"], 0, 2, 2,
     "A busca linear termina assim que encontra um elemento igual ao procurado. O primeiro 3 "
     "esta na posicao 1, entao a busca para ali e a posicao 3 nem chega a ser examinada."),

    ("Busca sequencial", "linear", [14, 8, 21, 5, 17, 2, 11], 10,
     "Quantas comparacoes a busca linear faz ate concluir que o valor 10 nao esta na lista?",
     ["1", "4", "7", "8"], 2, 2, 2,
     "Para afirmar que o valor nao existe e preciso verificar todos os elementos. A lista "
     "tem 7, entao sao 7 comparacoes: e o pior caso, O(n)."),

    # ── Ordenacao por comparacao ─────────────────────────────────
    ("Ordenacao por comparacao", "bubble", [6, 2, 8, 4, 1], None,
     "Como fica a lista ao final da primeira passada do Bubble Sort?",
     ["[2, 6, 4, 1, 8]", "[1, 2, 4, 6, 8]", "[2, 4, 6, 1, 8]", "[6, 2, 4, 1, 8]"], 0, 2, 2,
     "Na primeira passada: 6 > 2 troca; 6 e 8 ja estao em ordem; 8 > 4 troca; 8 > 1 troca. "
     "O resultado e [2, 6, 4, 1, 8], com o 8 ja na posicao final."),

    ("Ordenacao por comparacao", "insertion", [3, 7, 4, 9, 2], None,
     "No Insertion Sort, o que acontece quando o valor 4 (posicao 2) e inserido na parte "
     "ordenada?",
     ["Nada, o 4 ja esta na posicao certa",
      "O 7 e deslocado uma posicao para a direita e o 4 ocupa a posicao 1",
      "O 7 e o 3 sao deslocados e o 4 ocupa a posicao 0",
      "O 4 troca de lugar com o 9"], 1, 2, 2,
     "A parte ordenada e [3, 7]. Como 7 > 4, o 7 vai para a direita; como 3 < 4, o "
     "deslocamento para. O 4 e inserido na posicao 1, resultando em [3, 4, 7, 9, 2]."),

    # ── Complexidade de algoritmos ───────────────────────────────
    ("Complexidade de algoritmos", "selection", [1, 3, 5, 7, 9], None,
     "A lista abaixo ja esta ordenada. Quantas comparacoes o Selection Sort faz mesmo assim?",
     ["0", "4", "10", "25"], 2, 3, 3,
     "O Selection Sort sempre percorre toda a parte nao ordenada para confirmar o menor: "
     "4 + 3 + 2 + 1 = 10 comparacoes, ou n(n - 1) / 2. Por isso ele e O(n²) ate no melhor "
     "caso, embora aqui nao faca nenhuma troca."),

    ("Complexidade de algoritmos", "binaria", [3, 6, 9, 12, 15, 18, 21, 24, 27, 30], 30,
     "A busca linear precisaria verificar os 10 elementos para encontrar o 30. Quantos "
     "elementos a busca binaria compara ate encontra-lo?",
     ["1", "4", "5", "10"], 1, 3, 3,
     "A busca binaria compara 15, 24, 27 e 30: quatro elementos. Cada comparacao descarta "
     "metade do que resta, o que explica a diferenca entre O(log n) e O(n)."),

    # ── Listas ───────────────────────────────────────────────────
    ("Listas", "linear", [17, 8, 42, 23, 5, 31], 42,
     "A busca linear vai encontrar o valor 42 na lista abaixo. Em qual indice ele esta?",
     ["Indice 3, pois e o terceiro elemento", "Indice 1", "Indice 2", "Indice 42"], 2, 1, 2,
     "Os indices comecam em 0. O 42 e o terceiro elemento, portanto esta no indice 2. A "
     "busca o encontra na terceira comparacao."),

    ("Listas", "insertion", [4, 1, 3, 9, 7], None,
     "No Insertion Sort, como fica a lista depois que os tres primeiros elementos estao "
     "ordenados entre si (fim da iteracao com i = 2)?",
     ["[1, 4, 3, 9, 7]", "[1, 3, 4, 7, 9]", "[1, 3, 4, 9, 7]", "[4, 1, 3, 9, 7]"], 2, 2, 2,
     "Com i = 1, o 1 e inserido antes do 4: [1, 4, 3, 9, 7]. Com i = 2, o 4 e deslocado e o "
     "3 entra na posicao 1: [1, 3, 4, 9, 7]. O 9 e o 7 ainda nao foram processados."),

    # ── Busca binaria ────────────────────────────────────────────
    ("Busca binaria", "binaria", [4, 9, 13, 18, 25, 31, 40], 9,
     "A busca binaria procura o valor 9. Depois de comparar com o elemento do meio (18), "
     "qual trecho continua sendo analisado?",
     ["[25, 31, 40]", "[4, 9, 13]", "[13, 18, 25]", "A lista inteira"], 1, 2, 2,
     "Como 18 > 9, o valor so pode estar a esquerda do meio. O 18 e tudo a sua direita sao "
     "descartados, e a busca continua em [4, 9, 13], encontrando o 9 no novo meio."),

    ("Busca binaria", "binaria", [2, 6, 10, 14, 18, 22, 26, 30], 15,
     "A busca binaria vai procurar o valor 15, que nao esta na lista. Quais elementos sao "
     "comparados, em ordem?",
     ["14, 18, 22", "2, 6, 10, 14, 18", "18, 14", "14, 22, 18"], 3, 3, 3,
     "Meio inicial: 14 < 15, descarta a esquerda. No trecho [18, 22, 26, 30] o meio e 22 > 15, "
     "descarta a direita. Resta [18]; 18 > 15 e o trecho fica vazio. Foram 3 comparacoes: "
     "14, 22 e 18."),

    # ── Ordenacao aplicada a listas ──────────────────────────────
    ("Ordenacao aplicada a listas", "merge", [6, 2, 9, 4, 7, 1], None,
     "O Merge Sort divide a lista ate trechos de um elemento antes de intercalar. Qual e o "
     "resultado da primeira intercalacao?",
     ["[2, 6]", "[2, 6, 9]", "[1, 2]", "[4, 7]"], 0, 3, 3,
     "A divisao segue primeiro pela metade esquerda: [6, 2, 9] → [6, 2] → [6] e [2]. A "
     "primeira intercalacao junta [6] com [2], produzindo [2, 6]. So depois o 9 entra."),

    ("Ordenacao aplicada a listas", "selection", [5, 3, 8, 1, 6], None,
     "Quantas trocas o Selection Sort faz para ordenar a lista abaixo?",
     ["2", "3", "4", "10"], 1, 3, 3,
     "Passada 1: troca 5 e 1. Passada 2: o 3 ja e o menor, sem troca. Passada 3: troca 8 e 5. "
     "Passada 4: troca 8 e 6. Sao 3 trocas; o Selection Sort faz no maximo n - 1. O Bubble "
     "Sort, na mesma lista, faria 5."),
]
