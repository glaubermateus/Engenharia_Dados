#LIB
from pathlib import Path

# SQL LOADER

def load_sql(relative_path):

    base_path = Path(__file__).resolve().parent.parent

    sql_path = (
        base_path / relative_path
    )

    with open(
        sql_path,
        "r",
        encoding="utf-8"
    ) as file:

        query = file.read()

    return query