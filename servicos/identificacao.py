"""Regra de identificacao do estudante.

Funcoes puras, sem Streamlit, para que a regra possa ser testada isoladamente.
"""

MIN_CARACTERES_APELIDO = 3
MAX_CARACTERES_APELIDO = 30


def normalizar_apelido(texto: str) -> str:
    """Remove os espacos das pontas; e esse o valor gravado."""
    return (texto or "").strip()


def validar_apelido(texto: str) -> list[str]:
    """Devolve a lista de erros; lista vazia significa apelido aceito."""
    apelido = normalizar_apelido(texto)
    if not apelido:
        return ["Informe uma identificacao para continuar."]
    if len(apelido) < MIN_CARACTERES_APELIDO:
        return [f"Use pelo menos {MIN_CARACTERES_APELIDO} caracteres."]
    if len(apelido) > MAX_CARACTERES_APELIDO:
        return [f"Use no maximo {MAX_CARACTERES_APELIDO} caracteres."]
    return []
