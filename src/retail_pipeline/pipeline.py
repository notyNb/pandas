from retail_pipeline.config import PipelineConfig
from retail_pipeline.extract import extract_raw_data
from retail_pipeline.load import create_database_engine, load_tables, write_processed_csv
from retail_pipeline.report import generate_reports, write_run_summary
from retail_pipeline.transform import build_analytics_model


def run_pipeline() -> None:
    config = PipelineConfig.load()
    config.ensure_directories()

    raw_data = extract_raw_data(config.raw_dir)
    tables = build_analytics_model(raw_data)

    write_processed_csv(tables, config.processed_dir)

    engine = create_database_engine(config.database_url)
    load_tables(engine, tables)

    reports = generate_reports(engine, config.sql_dir, config.reports_dir)
    write_run_summary(config.reports_dir, tables, reports)

    print("Pipeline finished successfully.")
    print(f"Database: {config.database_url}")
    print(f"Processed files: {config.processed_dir}")
    print(f"Reports: {config.reports_dir}")
