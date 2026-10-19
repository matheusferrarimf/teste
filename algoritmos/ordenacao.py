"""Algoritmos de ordenacao instrumentados para visualizacao.

Nenhuma funcao deste modulo conhece Streamlit. Elas recebem uma lista e
devolvem uma lista de PassoExecucao, o que permite testa-las isoladamente
e reaproveita-las em qualquer interface.
"""

from typing import List

from .base import PassoExecucao


def bubble_sort(entrada: List[int]) -> List[PassoExecucao]:
    a = list(entrada)
    n = len(a)
    passos: List[PassoExecucao] = []

    for i in range(n - 1):
        for j in range(n - 1 - i):
            passos.append(PassoExecucao(
                lista=list(a), foco=[j, j + 1], fixos=list(range(n - i, n)),
                tipo="comparacao",
                texto=f"Compara as posicoes {j} e {j + 1}: {a[j]} e {a[j + 1]}",
            ))
            if a[j] > a[j + 1]:
                maior, menor = a[j], a[j + 1]
                a[j], a[j + 1] = a[j + 1], a[j]
                passos.append(PassoExecucao(
                    lista=list(a), foco=[j, j + 1], fixos=list(range(n - i, n)),
                    tipo="troca",
                    texto=f"{maior} > {menor} — troca as posicoes {j} e {j + 1}",
                ))
        passos.append(PassoExecucao(
            lista=list(a), fixos=list(range(n - 1 - i, n)), tipo="ok",
            texto=f"Fim da passada {i + 1}: {a[n - 1 - i]} ficou na posicao final",
        ))

    passos.append(PassoExecucao(
        lista=list(a), fixos=list(range(n)), tipo="fim", texto="Lista ordenada",
    ))
    return passos


def selection_sort(entrada: List[int]) -> List[PassoExecucao]:
    a = list(entrada)
    n = len(a)
    passos: List[PassoExecucao] = []

    for i in range(n - 1):
        menor = i
        passos.append(PassoExecucao(
            lista=list(a), foco=[i], fixos=list(range(i)), tipo="ok",
            texto=f"Passada {i + 1}: assume {a[i]} (posicao {i}) como o menor",
        ))
        for j in range(i + 1, n):
            passos.append(PassoExecucao(
                lista=list(a), foco=[j, menor], fixos=list(range(i)),
                tipo="comparacao",
                texto=f"Compara {a[j]} com o menor atual {a[menor]}",
            ))
            if a[j] < a[menor]:
                menor = j
                passos.append(PassoExecucao(
                    lista=list(a), foco=[menor], fixos=list(range(i)), tipo="ok",
                    texto=f"Novo menor: {a[menor]} na posicao {menor}",
                ))
        if menor != i:
            x, y = a[i], a[menor]
            a[i], a[menor] = a[menor], a[i]
            passos.append(PassoExecucao(
                lista=list(a), foco=[i, menor], fixos=list(range(i)), tipo="troca",
                texto=f"Troca {x} e {y} — o menor vai para a posicao {i}",
            ))

    passos.append(PassoExecucao(
        lista=list(a), fixos=list(range(n)), tipo="fim", texto="Lista ordenada",
    ))
    return passos


def insertion_sort(entrada: List[int]) -> List[PassoExecucao]:
    a = list(entrada)
    n = len(a)
    passos: List[PassoExecucao] = []

    for i in range(1, n):
        chave = a[i]
        # A chave sai da lista e fica "na mao": a posicao i vira um buraco.
        passos.append(PassoExecucao(
            lista=list(a), foco=[i], fixos=list(range(i)), buraco=[i],
            chave=chave, tipo="ok",
            texto=f"Retira {chave} da posicao {i} para inserir na parte ordenada",
        ))
        j = i - 1
        while j >= 0 and a[j] > chave:
            passos.append(PassoExecucao(
                lista=list(a), foco=[j], fixos=list(range(i)), buraco=[j + 1],
                chave=chave, tipo="comparacao",
                texto=f"{a[j]} > {chave} — desloca {a[j]} uma posicao a direita",
            ))
            a[j + 1] = a[j]
            passos.append(PassoExecucao(
                lista=list(a), foco=[j + 1], fixos=list(range(i)), buraco=[j],
                chave=chave, tipo="troca",
                texto=f"{a[j + 1]} passa para a posicao {j + 1}; a posicao {j} fica aberta",
            ))
            j -= 1
        a[j + 1] = chave
        passos.append(PassoExecucao(
            lista=list(a), foco=[j + 1], fixos=list(range(i + 1)), tipo="troca",
            texto=f"Insere {chave} na posicao {j + 1}",
        ))

    passos.append(PassoExecucao(
        lista=list(a), fixos=list(range(n)), tipo="fim", texto="Lista ordenada",
    ))
    return passos


def merge_sort(entrada: List[int]) -> List[PassoExecucao]:
    """Merge Sort com divisao e conquista.

    A lista completa e sempre exibida; o trecho em processamento aparece
    em destaque, para que o estudante perceba a reducao do problema.
    """
    a = list(entrada)
    n = len(a)
    passos: List[PassoExecucao] = []

    def intercalar(inicio: int, meio: int, fim: int) -> None:
        esquerda = a[inicio:meio + 1]
        direita = a[meio + 1:fim + 1]
        passos.append(PassoExecucao(
            lista=list(a), foco=list(range(inicio, fim + 1)), tipo="ok",
            texto=f"Copia as duas metades e intercala {esquerda} com {direita}",
        ))

        def registrar(k: int, texto: str) -> None:
            # As posicoes a frente do ponteiro de escrita ainda guardam os
            # valores antigos do trecho; marca-las evita leitura equivocada.
            passos.append(PassoExecucao(
                lista=list(a), foco=[k], fixos=list(range(inicio, k)),
                buraco=list(range(k + 1, fim + 1)), tipo="troca", texto=texto,
            ))

        i = j = 0
        k = inicio
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] <= direita[j]:
                a[k] = esquerda[i]
                i += 1
            else:
                a[k] = direita[j]
                j += 1
            registrar(k, f"Menor valor da vez: {a[k]} vai para a posicao {k}")
            k += 1
        while i < len(esquerda):
            a[k] = esquerda[i]
            registrar(k, f"Restou {a[k]} na metade da esquerda — posicao {k}")
            i += 1
            k += 1
        while j < len(direita):
            a[k] = direita[j]
            registrar(k, f"Restou {a[k]} na metade da direita — posicao {k}")
            j += 1
            k += 1

        passos.append(PassoExecucao(
            lista=list(a), fixos=list(range(inicio, fim + 1)), tipo="ok",
            texto=f"Trecho das posicoes {inicio} a {fim} intercalado",
        ))

    def dividir(inicio: int, fim: int) -> None:
        if inicio >= fim:
            return
        meio = (inicio + fim) // 2
        passos.append(PassoExecucao(
            lista=list(a), foco=list(range(inicio, fim + 1)), tipo="comparacao",
            texto=f"Divide o trecho das posicoes {inicio} a {fim} ao meio",
        ))
        dividir(inicio, meio)
        dividir(meio + 1, fim)
        intercalar(inicio, meio, fim)

    dividir(0, n - 1)
    passos.append(PassoExecucao(
        lista=list(a), fixos=list(range(n)), tipo="fim", texto="Lista ordenada",
    ))
    return passos
