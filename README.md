# AlgoVis — protótipo de jogo para ensino de algoritmos

Trabalho de Conclusão de Curso — Sistemas de Informação — UNIDAVI
Matheus Ferrari dos Santos · 2026

Aplicação web em Python/Streamlit que apresenta desafios sobre algoritmos de ordenação
e busca e, após cada resposta, exibe a execução do algoritmo passo a passo.

---

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

A aplicação abre em `http://localhost:8501`. O banco SQLite é criado e populado
automaticamente na primeira execução, em `dados/algovis.db`. Para começar do zero,
basta apagar esse arquivo.

## Como rodar os testes

```bash
pip install pytest
pytest testes/ -v
```

São 130 verificações cobrindo os geradores de passos, o vínculo entre passos e
linhas do pseudocódigo, as regras de negócio, a camada de dados, as regras de
sinalização do dashboard, a identificação do aluno, o resumo da visita e os
pop-ups (via `streamlit.testing.v1.AppTest`, sobre um banco temporário).

---

## Arquitetura em camadas

A separação existe por um motivo prático, não decorativo: os testes em `testes/`
exercitam `dados/` e `servicos/` sem subir a interface. Se a lógica estivesse
misturada ao Streamlit, isso não seria possível.

```
algovis/
├── app.py                    Configuração da página e roteamento entre telas
├── requirements.txt
├── .streamlit/config.toml    Tema (azul institucional sobre fundo claro)
│
├── paginas/                  CAMADA DE APRESENTAÇÃO
│   ├── inicio.py             Identificação do aluno e escolha da trilha
│   ├── jogo.py               Questões, feedback e visualização
│   ├── cadastro.py           CRUD das perguntas teóricas
│   ├── avaliacao.py          Questionário aplicado ao final da rodada
│   └── dashboard.py          Análise das avaliações coletadas
│
├── componentes/              APRESENTAÇÃO — elementos reutilizáveis
│   ├── estilo.py             Tokens de cor, tipografia e CSS
│   ├── visualizacao.py       Renderização da lista e animação
│   ├── dialogos.py           Pop-ups de identificação e de fim de módulo
│   ├── fluxo.py              Início de rodada, conclusão de módulo e fim da visita
│   └── ui.py                 Etiquetas, KPIs, barras de média
│
├── servicos/                 CAMADA DE APLICAÇÃO (regras de negócio)
│   ├── controle_questao.py   Montagem da rodada e validação de respostas
│   ├── identificacao.py      Validação do apelido do aluno
│   ├── pontuacao.py          Pesos, pontuação, progressão e resumo da visita
│   └── analise.py            Sinalização de respostas sem atenção
│
├── algoritmos/               CAMADA DE DOMÍNIO
│   ├── base.py               PassoExecucao
│   ├── ordenacao.py          Bubble, Selection, Insertion, Merge
│   ├── busca.py              Linear e binária
│   ├── pseudocodigo.py       Pseudocódigo de cada algoritmo e rótulos das linhas
│   └── __init__.py           Registro MOTORES
│
├── dados/                    CAMADA DE DADOS
│   ├── banco.py              Conexão e esquema SQLite
│   ├── repositorio.py        Único lugar do projeto que escreve SQL
│   └── seed.py               Carga inicial
│
└── testes/
    ├── test_algoritmos.py
    ├── test_fluxo.py
    ├── test_pseudocodigo.py
    └── test_regras.py
```

---

## A ideia central: algoritmos que devolvem passos

Cada algoritmo, em vez de apenas ordenar, devolve a sequência de estados
intermediários pelos quais a lista passou:

```python
@dataclass
class PassoExecucao:
    lista: List[int]         # estado completo neste momento
    foco: List[int]          # em destaque (comparados/movidos)
    fixos: List[int]         # já posicionados em definitivo
    descartados: List[int]   # fora do espaço de busca (busca binária)
    buraco: List[int]        # conteúdo ainda não válido
    tipo: str                # comparacao | troca | ok | fim
    texto: str               # descrição em linguagem natural
    chave: int               # valor "na mão" (Insertion Sort)
    linha: str               # rótulo da linha do pseudocódigo deste quadro
```

A camada de apresentação apenas percorre essa lista e desenha cada quadro. Para
acrescentar um algoritmo novo, escreva o gerador e registre-o em
`algoritmos/__init__.py`; nenhuma outra camada precisa mudar.

### Por que existe o campo `buraco`

Insertion Sort e Merge Sort deslocam elementos: a cópia já foi feita, mas a posição
de origem ainda não foi sobrescrita. Nesse instante a lista mostra um valor
duplicado. Sem marcação, o aluno veria `[5, 5, 8, 1]` e concluiria que o algoritmo
está errado. Marcada como tracejada, a posição comunica o que de fato é: espaço
aberto esperando o próximo valor. Vale mencionar isso na defesa — é uma decisão de
design didático, não um detalhe de implementação.

---

## Sistema de pesos

| Tipo | Peso | Pontos | O que exige do aluno |
|---|---|---|---|
| Teórica | 1 | 10 | Reconhecimento de conceito |
| Com visualização | 2 | 20 | Prever o comportamento do algoritmo |
| Teórica avançada | 3 | 30 | Análise e comparação entre algoritmos |

O peso aparece na tela **antes** de o aluno responder. Em gamificação, o peso só
influencia o comportamento se for conhecido de antemão.

---

## Regras de negócio implementadas

| Código | Regra | Onde está |
|---|---|---|
| RN01 | Exatamente uma alternativa correta por questão | `controle_questao.validar_resposta` |
| RN02 | De três a cinco alternativas | `paginas/cadastro.py` |
| RN04 | Feedback sempre exibido após a resposta | `paginas/jogo.py` |
| RN05 | Acerto soma peso × 10; erro não subtrai | `pontuacao.pontos_da_questao` |
| RN07 | Listas de 5 a 10 elementos | `controle_questao.validar_lista` |
| RN08 | Busca binária exige lista ordenada | `controle_questao.validar_lista` |
| RN09 | Animação só aparece após a resposta | `paginas/jogo.py` |
| RN10 | Avanço de nível exige 70% de acertos | `pontuacao.liberou_proximo_nivel` |
| RN11 | Ordem das questões embaralhada por sessão | `controle_questao.montar_rodada` |
| RN12 | Sessão registra data, acertos, erros e pontuação | `repositorio.finalizar_sessao` |

---

## Sinalização de respostas para a pesquisa

O dashboard **sinaliza**, mas nunca apaga. Três regras, em `servicos/analise.py`:

1. Média abaixo de 6 segundos por questão
2. Questionário de avaliação respondido em menos de 12 segundos
3. Mesma nota em todos os critérios (*straight-lining*)

O botão "Excluir sessões sinalizadas dos cálculos" recalcula as médias na hora, o
que permite relatar no Capítulo 4 o impacto do descarte sobre os resultados.

**Importante para a metodologia:** descreva esses critérios no trabalho *antes* da
coleta. Critério criado depois de ver os dados é frágil metodologicamente.

---

## Ajustes necessários no texto do TCC

- O DER descrito no material anterior precisa ganhar a entidade `avaliacao`
  (`id_avaliacao`, `id_sessao`, `facilidade`, `visualizacao`, `entendimento`,
  `nivel`, `comentario`, `tempo_preenchimento`, `data_hora`), que não estava
  prevista e é onde ficam os dados da validação.
- A entidade `progresso` está no DER mas ainda não foi implementada. Ou implemente,
  ou remova do diagrama — diagrama e código precisam bater na defesa.
- A tabela `questao` tem a coluna `editavel`, que separa as questões teóricas
  cadastráveis das questões com visualização, fixas em código. Inclua-a no
  dicionário de dados.

---

## Limitações conhecidas

- A animação usa `time.sleep()` dentro de um *placeholder*. Funciona bem, mas
  bloqueia a interação enquanto executa; por isso existe também a navegação manual
  passo a passo.
- Não há autenticação. O aluno se identifica por um apelido livre, adequado a uma
  coleta em sala mas não a uso aberto.
- O Merge Sort exibe a lista inteira durante a intercalação, com as posições ainda
  não reescritas marcadas. Uma representação em árvore seria mais fiel à divisão e
  conquista, e fica como trabalho futuro.
