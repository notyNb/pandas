# Retail Analytics Data Pipeline

Projeto pessoal de engenharia de dados para importar, limpar, transformar, armazenar e analisar dados de vendas de varejo.

O objetivo é demonstrar um fluxo completo e reprodutível: dados brutos em CSV entram na camada `data/raw`, passam por validações e transformações com Pandas, são carregados em um banco SQL e geram relatórios analíticos prontos para consumo.

## Por Que Este Projeto Chama Atenção

- Pipeline funcional de ponta a ponta, com execução por linha de comando.
- Dados brutos com problemas reais: nulos, duplicidades, textos fora de padrão, status inconsistentes e valores inválidos.
- Camadas claras de dados: `raw`, `processed`, `warehouse` e `reports`.
- Carga em banco relacional via SQLAlchemy.
- SQLite por padrão para facilitar a avaliação por recrutadores.
- Suporte a PostgreSQL usando `DATABASE_URL`.
- Consultas SQL versionadas em `sql/`.
- Testes automatizados para regras críticas de transformação.
- README orientado a portfolio, explicando arquitetura, execução e decisões técnicas.

## Arquitetura

```text
data/raw/*.csv
        |
        v
src/retail_pipeline/extract.py
        |
        v
src/retail_pipeline/transform.py
        |
        v
data/processed/*.csv
        |
        v
SQLite ou PostgreSQL
        |
        v
sql/*.sql + data/reports/*.csv
```

## Estrutura

```text
.
├── data/
│   ├── raw/                  # CSVs originais
│   ├── processed/            # CSVs limpos gerados pelo pipeline
│   ├── warehouse/            # Banco SQLite local
│   └── reports/              # Relatórios analíticos exportados
├── docs/                     # Dicionário de dados e pitch do projeto
├── sql/                      # Consultas SQL analíticas
├── src/retail_pipeline/      # Código do pipeline
├── tests/                    # Testes automatizados
├── .env.example              # Exemplo de configuração
├── requirements.txt
└── run_pipeline.py
```

## Como Executar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -e ".[dev]"
```

Execute o pipeline:

```bash
retail-pipeline
```

Também é possível executar com `python run_pipeline.py` após instalar o projeto em modo editável.

Ao final, serão gerados:

- `data/processed/clean_customers.csv`
- `data/processed/clean_products.csv`
- `data/processed/clean_orders.csv`
- `data/warehouse/retail.db`
- `data/reports/monthly_revenue.csv`
- `data/reports/top_products.csv`
- `data/reports/customer_segments.csv`
- `data/reports/data_quality_checks.csv`
- `data/reports/pipeline_run_summary.json`

## Usando PostgreSQL

Por padrão o projeto usa SQLite para facilitar a execução local. Para usar PostgreSQL, configure a variável `DATABASE_URL`.

Exemplo:

```bash
set DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/retail_analytics
python run_pipeline.py
```

No PowerShell:

```powershell
$env:DATABASE_URL="postgresql+psycopg2://usuario:senha@localhost:5432/retail_analytics"
python run_pipeline.py
```

## Regras De Tratamento

- Remove duplicidades por chave natural.
- Padroniza nomes, e-mails, cidades, UFs, categorias e status.
- Converte datas, quantidades e valores monetários.
- Remove pedidos cancelados da tabela fato analítica.
- Descarta registros sem chave obrigatória.
- Corrige valores negativos ou zerados quando invalidam uma venda.
- Calcula `gross_revenue`, `discount_amount` e `net_revenue`.
- Cria dimensões `dim_customers`, `dim_products` e fato `fact_orders`.

## Consultas Analíticas

As queries em `sql/` respondem perguntas comuns de negócio:

- Receita mensal, pedidos e ticket médio.
- Produtos mais vendidos por receita líquida.
- Segmentação de clientes por frequência e valor comprado.
- Checks de qualidade para integridade entre fato e dimensões.

## Documentação Para Recrutadores

- [Dicionário de dados](docs/data_dictionary.md)
- [Pitch do projeto](docs/portfolio_pitch.md)

## Testes

Execute:

```bash
pytest
```

Os testes cobrem regras de transformação, remoção de duplicidade, padronização e cálculo de receita.

## Publicando No GitHub

Depois de criar um repositório vazio no GitHub:

```bash
git remote add origin https://github.com/seu-usuario/retail-analytics-pipeline.git
git branch -M main
git push -u origin main
```

## Próximos Passos Possíveis

- Orquestrar o pipeline com Airflow ou Prefect.
- Criar dashboard em Power BI, Metabase ou Streamlit.
- Adicionar validação com Great Expectations.
- Publicar a base PostgreSQL em Docker Compose.
- Criar camada incremental com controle de watermark.

## Competências Demonstradas

Python, Pandas, SQL, modelagem dimensional, qualidade de dados, ETL, PostgreSQL, SQLite, Git, testes automatizados e documentação técnica.
