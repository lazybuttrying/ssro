from pathlib import Path

import duckdb
import pandas as pd


class DuckDBStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def write_df(self, table_name: str, df: pd.DataFrame) -> None:
        with duckdb.connect(str(self.db_path)) as con:
            con.register("tmp_df", df)
            sql = "CREATE OR REPLACE TABLE " + table_name + " AS SELECT * FROM tmp_df"
            con.execute(sql)

    def read_df(self, table_name: str) -> pd.DataFrame:
        with duckdb.connect(str(self.db_path)) as con:
            sql = "SELECT * FROM " + table_name
            return con.execute(sql).fetchdf()
