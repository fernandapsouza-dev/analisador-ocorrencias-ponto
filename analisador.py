"""Identifica inconsistências simples em registros fictícios de ponto."""

from datetime import datetime
from pathlib import Path

import pandas as pd


ARQUIVO_ENTRADA = Path("dados_exemplo.csv")
ARQUIVO_SAIDA = Path("resultado_exemplo.csv")

COLUNAS_OBRIGATORIAS = [
    "funcionario",
    "data",
    "entrada",
    "saida_almoco",
    "retorno_almoco",
    "saida",
]

COLUNAS_HORARIOS = [
    "entrada",
    "saida_almoco",
    "retorno_almoco",
    "saida",
]

NOMES_CAMPOS = {
    "entrada": "entrada",
    "saida_almoco": "saída para almoço",
    "retorno_almoco": "retorno do almoço",
    "saida": "saída",
}


def texto_limpo(valor: object) -> str:
    """Converte valores vazios do Pandas em texto vazio."""
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def horario_em_minutos(horario: str) -> int:
    """Converte HH:MM em minutos desde a meia-noite."""
    convertido = datetime.strptime(horario, "%H:%M")
    return convertido.hour * 60 + convertido.minute


def analisar_registro(registro: pd.Series) -> list[str]:
    """Retorna todas as ocorrências encontradas em uma linha."""
    ocorrencias: list[str] = []
    horarios = {campo: texto_limpo(registro[campo]) for campo in COLUNAS_HORARIOS}

    ausentes = [NOMES_CAMPOS[campo] for campo, valor in horarios.items() if not valor]
    if ausentes:
        ocorrencias.append(f"Marcação ausente: {', '.join(ausentes)}")
        quantidade = len(COLUNAS_HORARIOS) - len(ausentes)
        ocorrencias.append(f"Quantidade de marcações: {quantidade} de 4")

    minutos: dict[str, int] = {}
    invalidos: list[str] = []
    for campo, valor in horarios.items():
        if not valor:
            continue
        try:
            minutos[campo] = horario_em_minutos(valor)
        except ValueError:
            invalidos.append(f"{NOMES_CAMPOS[campo]} ({valor})")

    if invalidos:
        ocorrencias.append(f"Formato de horário inválido: {', '.join(invalidos)}")

    valores_repetidos: list[str] = []
    valores_validos = [valor for valor in horarios.values() if valor]
    for valor in dict.fromkeys(valores_validos):
        campos = [
            NOMES_CAMPOS[campo]
            for campo, horario in horarios.items()
            if horario == valor
        ]
        if len(campos) > 1:
            valores_repetidos.append(f"{valor} ({' e '.join(campos)})")

    if valores_repetidos:
        ocorrencias.append(f"Horários duplicados: {', '.join(valores_repetidos)}")

    todos_validos = len(minutos) == len(COLUNAS_HORARIOS)
    if todos_validos and not valores_repetidos:
        sequencia = [minutos[campo] for campo in COLUNAS_HORARIOS]
        if sequencia != sorted(sequencia) or len(set(sequencia)) != len(sequencia):
            ocorrencias.append("Ordem cronológica inconsistente")

    return ocorrencias


def validar_colunas(dados: pd.DataFrame) -> None:
    """Interrompe a execucao quando a planilha nao tem as colunas esperadas."""
    faltantes = [coluna for coluna in COLUNAS_OBRIGATORIAS if coluna not in dados.columns]
    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(faltantes)}")


def executar() -> None:
    """Lê a entrada, analisa os registros e grava somente as inconsistências."""
    dados = pd.read_csv(ARQUIVO_ENTRADA, sep=";", dtype=str)
    validar_colunas(dados)

    resultados: list[dict[str, str]] = []
    for _, registro in dados.iterrows():
        ocorrencias = analisar_registro(registro)
        if ocorrencias:
            resultados.append(
                {
                    "funcionario": texto_limpo(registro["funcionario"]),
                    "data": texto_limpo(registro["data"]),
                    "ocorrencias": " | ".join(ocorrencias),
                }
            )

    resultado = pd.DataFrame(
        resultados,
        columns=["funcionario", "data", "ocorrencias"],
    )
    resultado.to_csv(ARQUIVO_SAIDA, sep=";", index=False, encoding="utf-8-sig")

    total_registros = len(dados)
    total_inconsistencias = len(resultado)
    print(f"Registros analisados: {total_registros}")
    print(f"Registros com inconsistências: {total_inconsistencias}")
    print(f"Resultado salvo em: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    executar()
