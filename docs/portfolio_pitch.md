# Pitch Para Portfolio

Este projeto simula um cenário real de engenharia de dados em uma empresa de varejo: arquivos CSV chegam com problemas de qualidade e precisam ser transformados em uma base confiável para análise.

O pipeline foi desenvolvido em Python com Pandas e SQLAlchemy, aplicando limpeza, padronização, deduplicação, validação de integridade entre dimensões e fato, carga em banco relacional e geração de relatórios analíticos em CSV.

## Problema Resolvido

Dados transacionais brutos geralmente chegam com inconsistências: clientes duplicados, datas inválidas, produtos sem custo, pedidos cancelados, chaves inexistentes e campos textuais fora de padrão. O projeto resolve esse problema criando um fluxo reprodutível que transforma esses arquivos em tabelas analíticas confiáveis.

## Resultado

Ao executar um único comando, o pipeline gera uma base relacional com `dim_customers`, `dim_products` e `fact_orders`, além de relatórios de receita mensal, produtos mais vendidos e segmentação de clientes.

## Competências Que O Projeto Evidencia

- Construção de pipeline ETL com Python.
- Limpeza e validação de dados com Pandas.
- Modelagem dimensional simples.
- Persistência em banco SQL.
- Consultas analíticas versionadas.
- Testes automatizados.
- Documentação orientada a negócio e tecnologia.
