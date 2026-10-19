"""Dashboard de analise das sessoes e das avaliacoes coletadas."""

import pandas as pd
import streamlit as st

from componentes.estilo import CORES, titulo
from componentes.ui import kpi, medida
from dados import repositorio
from servicos.analise import (CRITERIOS, LIMITE_SEG_AVALIACAO,
                              LIMITE_SEG_POR_QUESTAO, enriquecer,
                              medias_por_criterio, resumo)


def _regras() -> None:
    st.markdown("#### Regras de sinalizacao")
    regras = [
        (f"Menos de {LIMITE_SEG_POR_QUESTAO}s por questao",
         "Tempo insuficiente para ler o enunciado e as alternativas"),
        (f"Avaliacao em menos de {LIMITE_SEG_AVALIACAO}s",
         "Questionario respondido sem leitura dos criterios"),
        ("Mesma nota em todos os criterios",
         "Padrao uniforme, indicio de resposta automatica"),
    ]
    for titulo_regra, descricao in regras:
        st.markdown(
            f'<div class="av-card" style="background:{CORES["amber_soft"]};'
            f'border-color:#F0D0A8;margin-bottom:8px">'
            f'<strong style="color:{CORES["amber"]};font-size:13.5px">{titulo_regra}</strong>'
            f'<div style="color:{CORES["ink2"]};font-size:12.5px">{descricao}</div></div>',
            unsafe_allow_html=True,
        )
    st.caption(
        "A sinalizacao nao apaga nada. A decisao de descartar continua sendo do "
        "pesquisador, e o criterio precisa estar descrito na metodologia."
    )


def _medias(base: list) -> None:
    st.markdown("#### Medias por criterio")
    medias = medias_por_criterio(base)
    for chave, rotulo, _ in CRITERIOS:
        nota = medias[chave]
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;align-items:baseline">'
            f'<span style="font-size:13.5px;color:{CORES["ink2"]}">{rotulo}</span>'
            f'<strong style="color:{CORES["blue"]}">{nota:.1f}</strong></div>'
            f"{medida(nota)}",
            unsafe_allow_html=True,
        )
        st.markdown("")
    st.caption("Escala de 1 a 5. Alterne o filtro acima para ver o impacto das sessoes sinalizadas.")


def _tabela(sessoes: list, ocultar: bool) -> None:
    st.markdown("#### Sessoes")
    linhas = []
    for s in sessoes:
        if ocultar and not s["valida"]:
            continue
        linhas.append({
            "Participante": s["apelido"],
            "Conteudo": s["conteudo"],
            "Acertos": f"{s['acertos']}/{s['total_questoes']}",
            "Pontos": s["pontuacao_total"],
            "Tempo/questao": f"{s['tempo_medio']:.0f}s",
            "Avaliacao": " · ".join(
                str(s[c]) for c, _, _ in CRITERIOS if s.get(c) is not None
            ) or "—",
            "Situacao": "valida" if s["valida"] else " · ".join(s["motivos"]),
        })

    if not linhas:
        st.info("Nenhuma sessao registrada ainda. Jogue uma rodada para gerar dados.")
        return

    st.dataframe(pd.DataFrame(linhas), use_container_width=True, hide_index=True)

    comentarios = [s for s in sessoes if s.get("comentario")]
    if comentarios:
        with st.expander(f"Comentarios abertos ({len(comentarios)})"):
            for s in comentarios:
                marca = "" if s["valida"] else " (sessao sinalizada)"
                st.markdown(f"**{s['apelido']}**{marca}: {s['comentario']}")


def _questoes_dificeis() -> None:
    dados = repositorio.estatisticas_por_questao()
    if not dados:
        return
    st.markdown("#### Questoes com maior indice de erro")
    st.caption("Util para revisar enunciados ambiguos ou conteudos mal compreendidos.")
    linhas = [{
        "Questao": d["enunciado"][:80] + ("..." if len(d["enunciado"]) > 80 else ""),
        "Tipo": d["tipo_questao"],
        "Peso": d["peso"],
        "Respostas": d["respostas"],
        "Acerto": f"{d['acertos'] / d['respostas'] * 100:.0f}%",
    } for d in dados[:10]]
    st.dataframe(pd.DataFrame(linhas), use_container_width=True, hide_index=True)


def render() -> None:
    titulo(
        "Dashboard de avaliacao",
        eyebrow="pesquisa",
        apoio="Cruze as notas do questionario com o tempo gasto para identificar "
              "respostas dadas sem atencao.",
    )

    sessoes = enriquecer(repositorio.listar_sessoes_avaliadas())
    if not sessoes:
        st.info("Nenhuma sessao concluida ainda. Jogue uma rodada para gerar dados.")
        return

    validas = [s for s in sessoes if s["valida"]]
    sinalizadas = len(sessoes) - len(validas)

    ocultar = st.toggle("Excluir sessoes sinalizadas dos calculos", value=False)
    base = validas if ocultar else sessoes
    r = resumo(base)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi("Sessoes registradas", str(len(sessoes)))
    with col2:
        kpi("Sinalizadas para descarte", str(sinalizadas), alerta=sinalizadas > 0)
    with col3:
        kpi("Tempo medio por questao", f"{r['tempo_medio']:.0f}s")
    with col4:
        kpi("Aproveitamento medio", f"{r['aproveitamento']:.0f}%")

    st.caption(f"{len(base)} de {len(sessoes)} sessoes consideradas nos calculos.")
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        _medias(base)
    with col_b:
        _regras()

    st.divider()
    _tabela(sessoes, ocultar)
    st.divider()
    _questoes_dificeis()
