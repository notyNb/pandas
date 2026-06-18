import pandas as pd

from retail_pipeline.transform import (
    build_analytics_model,
    transform_customers,
    transform_orders,
    transform_products,
)


def test_transform_customers_standardizes_and_deduplicates():
    raw = pd.DataFrame(
        {
            "customer_id": ["c001", "C001", None],
            "customer_name": [" ana  silva ", "ANA SILVA", "Sem Id"],
            "email": ["ANA@EMAIL.COM", "ana.new@email.com", "missing@email.com"],
            "city": ["sao paulo", "Sao Paulo", "Rio"],
            "state": ["sao paulo", "SP", "RJ"],
            "signup_date": ["2023-01-01", "bad-date", "2023-01-03"],
        }
    )

    result = transform_customers(raw)

    assert len(result) == 1
    assert result.loc[0, "customer_id"] == "C001"
    assert result.loc[0, "email"] == "ana.new@email.com"
    assert result.loc[0, "state"] == "SP"


def test_transform_orders_filters_invalid_rows_and_calculates_revenue():
    raw = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4"],
            "order_date": ["2024-01-01", "2024-01-02", "bad-date", "2024-01-04"],
            "customer_id": ["c1", "c1", "c1", "c1"],
            "product_id": ["p1", "p1", "p1", "p1"],
            "quantity": [2, 0, 1, 1],
            "unit_price": [100, 100, 100, 100],
            "discount_pct": [0.1, 0, 0, 0],
            "status": ["Delivered", "Delivered", "Delivered", "Cancelled"],
        }
    )

    result = transform_orders(raw)

    assert len(result) == 1
    assert result.loc[0, "order_id"] == "O1"
    assert result.loc[0, "gross_revenue"] == 200
    assert result.loc[0, "net_revenue"] == 180


def test_build_analytics_model_enforces_dimension_integrity():
    raw = {
        "customers": pd.DataFrame(
            {
                "customer_id": ["C1"],
                "customer_name": ["Ana"],
                "email": ["ana@email.com"],
                "city": ["Sao Paulo"],
                "state": ["SP"],
                "signup_date": ["2023-01-01"],
            }
        ),
        "products": pd.DataFrame(
            {
                "product_id": ["P1"],
                "product_name": ["Mouse"],
                "category": ["Acessorios"],
                "unit_cost": [20],
            }
        ),
        "orders": pd.DataFrame(
            {
                "order_id": ["O1", "O2"],
                "order_date": ["2024-01-01", "2024-01-02"],
                "customer_id": ["C1", "C999"],
                "product_id": ["P1", "P1"],
                "quantity": [1, 1],
                "unit_price": [100, 100],
                "discount_pct": [0, 0],
                "status": ["Delivered", "Delivered"],
            }
        ),
    }

    result = build_analytics_model(raw)

    assert len(result["fact_orders"]) == 1
    assert result["fact_orders"].iloc[0]["order_id"] == "O1"


def test_transform_products_removes_negative_costs():
    raw = pd.DataFrame(
        {
            "product_id": ["P1", "P2"],
            "product_name": ["Mouse", "Invalid"],
            "category": ["Acessorios", "Outros"],
            "unit_cost": [20, -1],
        }
    )

    result = transform_products(raw)

    assert result["product_id"].tolist() == ["P1"]
