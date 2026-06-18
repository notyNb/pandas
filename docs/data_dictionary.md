# Dicionário De Dados

## dim_customers

| Coluna | Descrição |
| --- | --- |
| customer_id | Identificador único do cliente. |
| customer_name | Nome padronizado do cliente. |
| email | E-mail em letras minúsculas. |
| city | Cidade padronizada. |
| state | UF padronizada. |
| signup_date | Data de cadastro tratada. |

## dim_products

| Coluna | Descrição |
| --- | --- |
| product_id | Identificador único do produto. |
| product_name | Nome padronizado do produto. |
| category | Categoria comercial do produto. |
| unit_cost | Custo unitário usado para estimar margem. |

## fact_orders

| Coluna | Descrição |
| --- | --- |
| order_id | Identificador único do pedido. |
| order_date | Data do pedido. |
| customer_id | Chave da dimensão de clientes. |
| product_id | Chave da dimensão de produtos. |
| quantity | Quantidade vendida. |
| unit_price | Preço unitário de venda. |
| discount_pct | Percentual de desconto aplicado. |
| status | Status válido do pedido. |
| gross_revenue | Receita bruta calculada. |
| discount_amount | Valor absoluto do desconto. |
| net_revenue | Receita líquida após desconto. |
