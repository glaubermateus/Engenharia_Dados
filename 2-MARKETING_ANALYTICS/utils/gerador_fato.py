# LIBS
import random
import pandas as pd
from utils.gerador_metricas import generate_metrics
from utils.dados_sujos import (canais_sujos, dispositivos_sujos)

# GENERATE FACT RECORD

def generate_fact_record(dimensions):

    metrics = generate_metrics()
    
    dim_date = dimensions["dim_data"]

    dim_campaign = dimensions["dim_campanha"]

    dim_region = dimensions["dim_regiao"]

    dim_audience = dimensions["dim_publico"]

    # RANDOM DATE
    
    random_date = random.choice(dim_date["data"].tolist())

    event_date = pd.to_datetime(random_date).strftime("%Y-%m-%d")

    # CAMPAIGN
    
    random_campaign = random.choice(dim_campaign.to_dict("records"))

    campaign_info = (

        f"{random_campaign['objetivo']}|"

        f"{random_campaign['nome_campanha']}|"

        f"{random_campaign['orcamento']}"
    )

    # RECORD

    row = {

        "data_evento":
        event_date,

        "nome_canal":
        random.choice(canais_sujos),

        "info_campanha":
        campaign_info,

        "id_regiao":
        random.choice(dim_region["id_regiao"].tolist()),

        "tipo_dispositivo":
        random.choice(dispositivos_sujos),

        "id_audiencia":
        random.choice(dim_audience["id_audiencia"].tolist()),

        "impressoes":
        metrics["impressoes"],

        "clicks":
        metrics["clicks"],

        "leads":
        metrics["leads"],

        "conversoes":
        metrics["conversoes"],

        "custo":
        metrics["custo"],

        "receita":
        metrics["receita"],

        "criado_em":
        pd.Timestamp.now()
    }

    return row