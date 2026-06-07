# LIBS
import random
import pandas as pd
from config.db import engine
from config.config import dados_dimensao, dados_fato
from utils.gerador_fato import generate_fact_record

# LOAD DIMENSIONS

dimensions = {
    "dim_data": pd.read_csv(dados_dimensao + "/dim_data.csv", sep=";", encoding="utf-8"),
    "dim_canal": pd.read_csv(dados_dimensao + "/dim_canal.csv", sep=";", encoding="utf-8"),
    "dim_dispositivo": pd.read_csv(dados_dimensao + "/dim_dispositivo.csv", sep=";", encoding="utf-8"),
    "dim_publico": pd.read_csv(dados_dimensao + "/dim_publico.csv", sep=";", encoding="utf-8"),
    "dim_regiao": pd.read_csv(dados_dimensao + "/dim_regiao.csv", sep=";", encoding="utf-8"),
    "dim_campanha": pd.read_csv(dados_dimensao + "/dim_campanha.csv", sep=";", encoding="utf-8")
}

# GENERATE RECORDS

records = []

for _ in range(50000):

    row = generate_fact_record(dimensions)

    records.append(row)

# DUPLICATES

duplicates = random.sample(records, k=1000)

records.extend(duplicates)

# DATAFRAME

fact_df = pd.DataFrame(records)

fact_df["id"] = (fact_df.index + 1)

# REORDER DATAFRAME
idx = 0
col = 'id'
value = fact_df.pop(col)
fact_df.insert(loc=idx, column=col, value=value)

# SHUFFLE

fact_df = fact_df.sample(frac=1).reset_index(drop=True)

# LOAD RAW

print(
    "\\nCarregando RAW..."
)

fact_df.to_sql("tb_raw_marketing", engine, schema="raw", if_exists="append", index=False)

fact_df.to_csv(dados_fato + "/tb_raw_marketing.csv", sep=";", index=False, encoding="utf-8")

print(
    "\\nRAW carregada com sucesso."
)