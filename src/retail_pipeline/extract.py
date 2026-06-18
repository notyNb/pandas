from pathlib import Path

import pandas as pd


def read_csv_dataset(raw_dir: Path, name: str) -> pd.DataFrame:
    path = raw_dir / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {path}")
    return pd.read_csv(path)


def extract_raw_data(raw_dir: Path) -> dict[str, pd.DataFrame]:
    return {
        "customers": read_csv_dataset(raw_dir, "customers"),
        "products": read_csv_dataset(raw_dir, "products"),
        "orders": read_csv_dataset(raw_dir, "orders"),
    }
