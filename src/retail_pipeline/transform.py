import pandas as pd


VALID_ORDER_STATUSES = {"delivered", "shipped", "processing"}
STATE_REPLACEMENTS = {
    "sao paulo": "SP",
    "sp": "SP",
    "rio de janeiro": "RJ",
    "rj": "RJ",
    "minas gerais": "MG",
    "mg": "MG",
    "bahia": "BA",
    "ba": "BA",
    "parana": "PR",
    "pr": "PR",
}


def _clean_text(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().str.replace(r"\s+", " ", regex=True)


def _title(series: pd.Series) -> pd.Series:
    return _clean_text(series).str.lower().str.title()


def transform_customers(customers: pd.DataFrame) -> pd.DataFrame:
    df = customers.copy()
    df.columns = df.columns.str.strip().str.lower()

    df = df.dropna(subset=["customer_id"])
    df["customer_id"] = _clean_text(df["customer_id"]).str.upper()
    df["customer_name"] = _title(df["customer_name"]).fillna("Unknown")
    df["email"] = _clean_text(df["email"]).str.lower()
    df["city"] = _title(df["city"]).fillna("Unknown")
    df["state"] = (
        _clean_text(df["state"])
        .str.lower()
        .map(STATE_REPLACEMENTS)
        .fillna(_clean_text(df["state"]).str.upper())
    )
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
    df["signup_date"] = df["signup_date"].fillna(pd.Timestamp("2023-01-01"))

    df = df.drop_duplicates(subset=["customer_id"], keep="last")
    return df[["customer_id", "customer_name", "email", "city", "state", "signup_date"]]


def transform_products(products: pd.DataFrame) -> pd.DataFrame:
    df = products.copy()
    df.columns = df.columns.str.strip().str.lower()

    df = df.dropna(subset=["product_id"])
    df["product_id"] = _clean_text(df["product_id"]).str.upper()
    df["product_name"] = _title(df["product_name"]).fillna("Unknown")
    df["category"] = _title(df["category"]).fillna("Uncategorized")
    df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce").fillna(0)
    df = df[df["unit_cost"] >= 0]

    df = df.drop_duplicates(subset=["product_id"], keep="last")
    return df[["product_id", "product_name", "category", "unit_cost"]]


def transform_orders(orders: pd.DataFrame) -> pd.DataFrame:
    df = orders.copy()
    df.columns = df.columns.str.strip().str.lower()

    df = df.dropna(subset=["order_id", "customer_id", "product_id"])
    df["order_id"] = _clean_text(df["order_id"]).str.upper()
    df["customer_id"] = _clean_text(df["customer_id"]).str.upper()
    df["product_id"] = _clean_text(df["product_id"]).str.upper()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["discount_pct"] = pd.to_numeric(df["discount_pct"], errors="coerce").fillna(0)
    df["status"] = _clean_text(df["status"]).str.lower()

    df = df.dropna(subset=["order_date", "quantity", "unit_price"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]
    df = df[df["status"].isin(VALID_ORDER_STATUSES)]
    df["discount_pct"] = df["discount_pct"].clip(lower=0, upper=0.8)

    df = df.drop_duplicates(subset=["order_id"], keep="last")
    df["gross_revenue"] = df["quantity"] * df["unit_price"]
    df["discount_amount"] = df["gross_revenue"] * df["discount_pct"]
    df["net_revenue"] = df["gross_revenue"] - df["discount_amount"]

    return df[
        [
            "order_id",
            "order_date",
            "customer_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount_pct",
            "status",
            "gross_revenue",
            "discount_amount",
            "net_revenue",
        ]
    ]


def build_analytics_model(raw: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    customers = transform_customers(raw["customers"])
    products = transform_products(raw["products"])
    orders = transform_orders(raw["orders"])

    orders = orders[orders["customer_id"].isin(customers["customer_id"])]
    orders = orders[orders["product_id"].isin(products["product_id"])]

    return {
        "dim_customers": customers,
        "dim_products": products,
        "fact_orders": orders,
    }
