# LIBS
from config.db import engine
from utils.gerador_dimensao import generate_dimensions
from config.config import dados_dimensao

# GENERATE DIMENSIONS

tables = generate_dimensions()

# LOAD TABLES

for table_name, df in tables.items():
    
    print(
        f"""
        Carregando:

        {table_name}
        """
    )
    
    df.to_sql(table_name,engine, schema="dimensions", if_exists="append", index=False)

    print(
        f"""
        {table_name}
        carregada com sucesso.
        """
    )

    csv_path = dados_dimensao + f"/{table_name}.csv"

    df.to_csv(csv_path, sep=";", index=False, encoding="utf-8")

    print(
        f"""
        {table_name} carregada com sucesso.
        """
    )