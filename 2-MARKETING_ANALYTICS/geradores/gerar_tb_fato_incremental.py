# LIBS
import pandas as pd
from config.db import engine
from utils.gerador_fato import generate_fact_record
from config.config import dados_dimensao, dados_fato
from utils.controle import get_max_raw_id

# CONFIG
NUM_NEW_RECORDS = 10000

# LOAD DIMENSIONS
tables = {
    "dim_data": pd.read_csv(dados_dimensao + "/dim_data.csv", sep=";", encoding="utf-8"),
    "dim_canal": pd.read_csv(dados_dimensao + "/dim_canal.csv", sep=";", encoding="utf-8"),
    "dim_dispositivo": pd.read_csv(dados_dimensao + "/dim_dispositivo.csv", sep=";", encoding="utf-8"),
    "dim_publico": pd.read_csv(dados_dimensao + "/dim_publico.csv", sep=";", encoding="utf-8"),
    "dim_regiao": pd.read_csv(dados_dimensao + "/dim_regiao.csv", sep=";", encoding="utf-8"),
    "dim_campanha": pd.read_csv(dados_dimensao + "/dim_campanha.csv", sep=";", encoding="utf-8")
}

# GET LAST RAW ID

max_id = get_max_raw_id()

# GENERATE RECORDS
records = [generate_fact_record(tables) for _ in range(NUM_NEW_RECORDS)]
fact_df = pd.DataFrame(records)

# RAW ID
fact_df["id"] = range(max_id + 1, max_id + 1 + len(fact_df))

new_max_id = fact_df["id"].max()
print(f"Novo último RAW ID: {new_max_id}")

# REORDER DATAFRAME
idx = 0
col = 'id'
value = fact_df.pop(col)
fact_df.insert(loc=idx, column=col, value=value)


# APPEND
fact_df.to_sql("tb_raw_marketing", engine, schema="raw", if_exists="append", index=False)

fact_df.to_csv(dados_fato + f"/tb_raw_marketing_incremental_{new_max_id}.csv", sep=";", index=False, encoding="utf-8")

print(
    "\nCarga incremental concluída."
)