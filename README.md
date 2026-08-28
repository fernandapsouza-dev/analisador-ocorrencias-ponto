# Analisador de Ocorrências de Ponto

Projeto de portfólio desenvolvido em Python e Pandas para identificar inconsistências simples em registros fictícios de ponto.

## Problema

A conferência manual de marcações pode consumir tempo e deixar passar campos vazios, horários duplicados ou registros fora da ordem esperada. Este projeto demonstra como uma verificação inicial pode ser automatizada antes da revisão humana.

## O que o programa verifica

- marcações ausentes;
- quantidade incompleta de marcações;
- horários em formato inválido;
- horários duplicados;
- sequência cronológica inconsistente.

## Tecnologias

- Python;
- Pandas;
- CSV;
- Git e GitHub.

## Estrutura do projeto

```text
analisador-ocorrencias-ponto/
|-- analisador.py
|-- dados_exemplo.csv
|-- resultado_exemplo.csv
|-- requirements.txt
`-- README.md
```

## Como executar

1. Tenha o Python instalado.
2. Instale a dependência:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute o programa na pasta do projeto:

   ```bash
   python analisador.py
   ```

4. Consulte o arquivo `resultado_exemplo.csv` gerado pelo programa.

## Exemplo

Se um registro estiver sem o retorno do almoço, o resultado indicará:

```text
Marcação ausente: retorno do almoço | Quantidade de marcações: 3 de 4
```

## Privacidade e limites

Todos os nomes, datas e horários deste repositório são fictícios e foram criados exclusivamente para demonstração. O projeto não utiliza dados reais de funcionários, não calcula folha de pagamento e não substitui a conferência de profissionais de RH ou Departamento Pessoal.

## Autora

Fernanda de Paula Souza - [GitHub](https://github.com/fernandapsouza-dev)
