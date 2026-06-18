from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def create_database_engine(database_url: str) -> Engine:
    return create_engine(database_url, future=True)


def write_processed_csv(tables: dict[str, pd.DataFrame], processed_dir: Path) -> None:
    processed_dir.mkdir(parents=True, exist_ok=True)
    for table_name, df in tables.items():
        file_name = table_name.replace("dim_", "clean_").replace("fact_", "clean_")
        df.to_csv(processed_dir / f"{file_name}.csv", index=False)


def load_tables(engine: Engine, tables: dict[str, pd.DataFrame]) -> None:
    for table_name, df in tables.items():
        df.to_sql(table_name, engine, if_exists="replace", index=False)


def execute_sql_file(engine: Engine, sql_path: Path) -> pd.DataFrame:
    query = sql_path.read_text(encoding="utf-8")
    with engine.connect() as connection:
        return pd.read_sql_query(text(query), connection)
