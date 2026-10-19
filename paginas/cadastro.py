"""Cadastro de perguntas teoricas.

Perguntas com visualizacao nao sao cadastradas aqui: cada uma depende do
gerador de passos de um algoritmo especifico, definido em codigo.
"""

import streamlit as st

from algoritmos import MOTORES
from componentes.estilo import CORES, titulo
from componentes.ui import etiqueta
from dados import repositorio
from servicos.pontuacao import PONTOS_POR_PESO


def _formulario(conteudos: list) -> None:
    st.markdown("#### Nova pergunta teorica")

    with st.form("nova_questao", clear_on_submit=True):
        enunciado = st.text_area(
            "Enunciado", placeholder="Ex.: Qual e a complexidade media do Merge Sort?"
        )

        st.markdown("**Alternativas**")
        alternativas = [
            st.text_input(f"Alternativa {chr(97 + i)}", key=f"alt_{i}")
            for i in range(4)
        ]
        correta = st.radio(
            "Qual e a alternativa correta?",
            options=list(range(4)),
            format_func=lambda i: f"Alternativa {chr(97 + i)}",
            horizontal=True,
        )

        col1, col2, col3 = st.columns(3)
        nome_conteudo = col1.selectbox("Conteudo", [c["nome"] for c in conteudos])
        nivel = col2.selectbox(
            "Nivel", [1, 2, 3],
            format_func=lambda n: {1: "1 — Basico", 2: "2 — Intermediario",
                                   3: "3 — Avancado"}[n],
        )
        peso = col3.selectbox(
            "Peso", [1, 2, 3], format_func=lambda p: f"{p} — {p * PONTOS_POR_PESO} pts"
        )

        explicacao = st.text_area(
            "Explicacao do feedback",
            placeholder="Texto mostrado ao aluno depois da resposta, explicando o porque.",
        )

        enviado = st.form_submit_button("Salvar pergunta", type="primary")

    if not enviado:
        return

    preenchidas = [a.strip() for a in alternativas if a.strip()]
    erros = []
    if not enunciado.strip():
        erros.append("Escreva o enunciado da pergunta.")
    if len(preenchidas) < 3:
        erros.append("Preencha ao menos tres alternativas (RN02).")
    if not alternativas[correta].strip():
        erros.append("A alternativa marcada como correta esta vazia.")
    if not explicacao.strip():
        erros.append("Escreva a explicacao exibida no feedback (RN04).")

    if erros:
        for e in erros:
            st.error(e)
        return

    id_conteudo = next(c["id_conteudo"] for c in conteudos if c["nome"] == nome_conteudo)
    # reindexa a correta considerando apenas as alternativas preenchidas
    indice_correta = preenchidas.index(alternativas[correta].strip())

    repositorio.inserir_questao_teorica(
        id_conteudo, enunciado.strip(), preenchidas, indice_correta,
        nivel, peso, explicacao.strip(),
    )
    st.success("Pergunta cadastrada.")
    st.rerun()


def _lista_teoricas() -> None:
    teoricas = repositorio.listar_questoes(tipo="teorica")
    st.markdown(f"#### Perguntas teoricas ({len(teoricas)})")

    for q in teoricas:
        with st.container(border=True):
            st.markdown(f"**{q['enunciado']}**")
            st.markdown(
                etiqueta(q["nome_conteudo"], "cinza")
                + etiqueta(f"nivel {q['nivel_dificuldade']}", "cinza")
                + etiqueta(f"peso {q['peso']}"),
                unsafe_allow_html=True,
            )
            for a in q["alternativas"]:
                marca = "✔" if a["correta"] else "·"
                st.caption(f"{marca} {a['texto']}")
            if st.button("Excluir", key=f"del_{q['id_questao']}"):
                if repositorio.excluir_questao(q["id_questao"]):
                    st.rerun()
                else:
                    st.error("Esta questao e fixa e nao pode ser excluida.")


def _lista_visuais() -> None:
    visuais = repositorio.listar_questoes(tipo="visual")
    st.markdown(f"#### Perguntas com visualizacao ({len(visuais)})")
    st.caption(
        "Fixas no codigo. Cada uma depende de um gerador de passos especifico do algoritmo, "
        "definido no modulo algoritmos/."
    )
    for q in visuais:
        with st.container(border=True):
            st.markdown(f"**{q['enunciado']}**")
            motor = MOTORES[q["chave_algoritmo"]]
            tags = (
                etiqueta(motor["nome"])
                + etiqueta(str(q["lista_inicial"]), "cinza")
                + etiqueta(f"peso {q['peso']}")
            )
            if q.get("valor_procurado") is not None:
                tags += etiqueta(f"alvo {q['valor_procurado']}", "ambar")
            st.markdown(tags, unsafe_allow_html=True)


def render() -> None:
    titulo(
        "Cadastrar perguntas",
        eyebrow="banco de questoes",
        apoio="Perguntas teoricas sao cadastradas aqui. As perguntas com codigo em "
              "execucao ficam fixas, pois dependem do motor de animacao de cada algoritmo.",
    )

    conteudos = repositorio.listar_conteudos()
    col_esq, col_dir = st.columns(2)
    with col_esq:
        _formulario(conteudos)
    with col_dir:
        aba1, aba2 = st.tabs(["Teoricas", "Com visualizacao"])
        with aba1:
            _lista_teoricas()
        with aba2:
            _lista_visuais()
