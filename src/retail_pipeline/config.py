from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class PipelineConfig:
    root_dir: Path = ROOT_DIR
    raw_dir: Path = ROOT_DIR / "data" / "raw"
    processed_dir: Path = ROOT_DIR / "data" / "processed"
    warehouse_dir: Path = ROOT_DIR / "data" / "warehouse"
    reports_dir: Path = ROOT_DIR / "data" / "reports"
    sql_dir: Path = ROOT_DIR / "sql"
    database_url: str = ""

    @classmethod
    def load(cls) -> "PipelineConfig":
        load_dotenv()
        warehouse_dir = ROOT_DIR / "data" / "warehouse"
        default_database_url = f"sqlite:///{warehouse_dir / 'retail.db'}"
        database_url = os.getenv("DATABASE_URL") or default_database_url
        return cls(database_url=database_url)

    def ensure_directories(self) -> None:
        for directory in [
            self.raw_dir,
            self.processed_dir,
            self.warehouse_dir,
            self.reports_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)
