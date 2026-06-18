import json
from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Engine

from retail_pipeline.load import execute_sql_file


REPORT_QUERIES = {
    "monthly_revenue": "monthly_revenue.sql",
    "top_products": "top_products.sql",
    "customer_segments": "customer_segments.sql",
    "data_quality_checks": "data_quality_checks.sql",
}


def generate_reports(engine: Engine, sql_dir: Path, reports_dir: Path) -> dict[str, pd.DataFrame]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    reports = {}
    for report_name, file_name in REPORT_QUERIES.items():
        report = execute_sql_file(engine, sql_dir / file_name)
        report.to_csv(reports_dir / f"{report_name}.csv", index=False)
        reports[report_name] = report
    return reports


def write_run_summary(
    reports_dir: Path,
    tables: dict[str, pd.DataFrame],
    reports: dict[str, pd.DataFrame],
) -> None:
    summary = {
        "loaded_tables": {name: len(df) for name, df in tables.items()},
        "generated_reports": {name: len(df) for name, df in reports.items()},
        "total_net_revenue": round(float(tables["fact_orders"]["net_revenue"].sum()), 2),
        "unique_customers_with_orders": int(tables["fact_orders"]["customer_id"].nunique()),
        "unique_products_sold": int(tables["fact_orders"]["product_id"].nunique()),
    }
    (reports_dir / "pipeline_run_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
