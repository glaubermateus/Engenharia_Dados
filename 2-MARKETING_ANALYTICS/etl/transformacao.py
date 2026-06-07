# LIBS
import numpy as np
import pandas as pd
from config.logger_config import logger
from config.config import dados_dimensao

dim_data = pd.read_csv(dados_dimensao + "/dim_data.csv", sep=";", encoding="utf-8")
dim_canal = pd.read_csv(dados_dimensao + "/dim_canal.csv", sep=";", encoding="utf-8")
dim_dispositivo = pd.read_csv(dados_dimensao + "/dim_dispositivo.csv", sep=";", encoding="utf-8")
dim_campanha = pd.read_csv(dados_dimensao + "/dim_campanha.csv", sep=";", encoding="utf-8")

# CLEAN CHANNEL NAME

def clean_channel_name(df):

    logger.info(
        "Padronizando canais..."
    )

    df["nome_canal"] = (

        df["nome_canal"]

        .astype(str)

        .str.strip()

        .str.upper()
    )

    replacements = {

        "GOOGLEADS": "GOOGLE ADS",

        " GOOGLE ADS ": "GOOGLE ADS",

        "GOOGLE ADS": "GOOGLE ADS",

        "META ADS": "META ADS",

        "LINKEDIN ADS": "LINKEDIN ADS",

        "LINKEDINADS": "LINKEDIN ADS",

        "TIKTOK ADS": "TIKTOK ADS",

        "EMAIL MARKETING": "EMAIL MARKETING"
    }

    df["nome_canal"] = (

        df["nome_canal"]

        .replace(replacements)
    )

    return df


# CLEAN DEVICE


def clean_device(df):

    logger.info(
        "Padronizando dispositivos..."
    )

    df["tipo_dispositivo"] = (

        df["tipo_dispositivo"]

        .astype(str)

        .str.strip()

        .str.upper()
    )

    replacements = {

        "CELULAR": "Celular",

        "COMPUTADOR": "Computador",

        "TABLET": "Tablet"
    }

    df["tipo_dispositivo"] = (

        df["tipo_dispositivo"]

        .replace(replacements)
    )

    return df


# SPLIT CAMPAIGN INFO


def split_campaign_info(df):

    logger.info(
        "Separando info_campanhas..."
    )

    split_cols = (

        df["info_campanha"]

        .astype(str)

        .str.split(
            "|",
            expand=True
        )
    )

    df["objetivo"] = (

        split_cols[0]
        .str.strip()
    )

    df["nome_campanha"] = (

        split_cols[1]
        .str.strip()
    )

    df["orcamento"] = pd.to_numeric(

        split_cols[2],

        errors="coerce"
    )

    return df


# CLEAN DATES


def clean_dates(df):

    logger.info(
        "Tratando datas..."
    )

    df["data_evento"] = pd.to_datetime(

        df["data_evento"],

        errors="coerce",

        dayfirst=True
    )

    invalid_dates = (

        df["data_evento"]
        .isna()
        .sum()
    )

    logger.info(
        f"{invalid_dates} datas inválidas."
    )

    df = df.dropna(
        subset=["data_evento"]
    )

    return df


# CLEAN COST


def clean_cost(df):

    logger.info(
        "Tratando coluna custo..."
    )

    df["custo"] = pd.to_numeric(

        df["custo"],

        errors="coerce"
    )

    return df


# CLEAN REVENUE


def clean_revenue(df):

    logger.info(
        "Tratando coluna receita..."
    )

    df["receita"] = pd.to_numeric(

        df["receita"],

        errors="coerce"
    )

    return df


# HANDLE NULLS


def handle_nulls(df):

    logger.info(
        "Tratando valores ausentes..."
    )

    df["custo"] = (

        df["custo"]
        .fillna(0)
    )

    df["receita"] = (

        df["receita"]
        .fillna(0)
    )

    return df


# REMOVE DUPLICATES


def remove_duplicates(df):

    before = len(df)

    df.drop_duplicates(subset=["id"], inplace=True)

    after = len(df)

    logger.info(
        f"{before - after} duplicidades removidas."
    )

    return df


# REMOVE INVALID METRICS


def remove_invalid_metrics(df):

    logger.info(
        "Removendo métricas inválidas..."
    )

    before = len(df)

    conditions = (

        (df["impressoes"] >= df["clicks"])

        &

        (df["clicks"] >= df["leads"])

        &

        (df["leads"] >= df["conversoes"])
    )

    df = df[conditions]

    after = len(df)

    logger.info(
        f"{before - after} registros inválidos removidos."
    )

    return df


# CAST TYPES


def cast_types(df):

    logger.info(
        "Convertendo tipos..."
    )

    int_columns = [

        "id_regiao",

        "id_audiencia",

        "impressoes",

        "clicks",

        "leads",

        "conversoes"
    ]

    for col in int_columns:

        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"
        ).astype(int)

    df[int_columns] = (

        df[int_columns]
        .fillna(0)
        .astype(int)
    )

    float_columns = [

        "custo",

        "receita",

        "orcamento"
    ]

    for col in float_columns:

        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"
        ).astype(float)

    return df


# ADD DIMENSION IDS

def add_dimension_ids(df):

    logger.info(
        "Relacionando IDs dimensão..."
    )

    # DATE

    dim_data["data"] = pd.to_datetime(
        dim_data["data"]
    )

    df = df.merge(

        dim_data,

        left_on="data_evento",

        right_on="data",

        how="left"
    )

    # CHANNEL

    dim_canal["nome_canal"] = (

        dim_canal["nome_canal"]

        .astype(str)

        .str.strip()

        .str.upper()
    )

    df = df.merge(

        dim_canal,

        on="nome_canal",

        how="left"
    )

    # DEVICE

    dim_dispositivo["tipo_dispositivo"] = (

        dim_dispositivo["tipo_dispositivo"]

        .astype(str)

        .str.strip()
    )

    df = df.merge(

        dim_dispositivo,

        on="tipo_dispositivo",

        how="left"
    )

    # CAMPAIGN

    df = df.merge(

        dim_campanha,

        on="nome_campanha",

        how="left"
    )

    # VALIDATE NULL IDS

    missing_ids = [

        "id_data",

        "id_canal",

        "id_dispositivo",

        "id_campanha"
    ]

    for col in missing_ids:

        null_count = df[col].isna().sum()

        logger.info(
            f"{null_count} registros sem {col}"
        )

    return df

# CREATE METRICS

def create_metrics(df):

    logger.info(
        "Criando métricas..."
    )

    df["taxa_cliques"] = np.where(

        df["impressoes"] > 0,

        df["clicks"] /
        df["impressoes"],

        0
    )

    df["taxa_conversao"] = np.where(

        df["leads"] > 0,

        df["conversoes"] /
        df["leads"],

        0
    )

    df["cpc"] = np.where(

        df["clicks"] > 0,

        df["custo"] /
        df["clicks"],

        0
    )

    df["roi"] = np.where(

        df["custo"] > 0,

        df["receita"] /
        df["custo"],

        0
    )

    return df


# REMOVE INFINITE VALUES


def remove_infinite_values(df):

    logger.info(
        "Removendo infinitos..."
    )

    df = df.replace(

        [np.inf, -np.inf],

        np.nan
    )

    return df


# FINAL CLEANUP


def final_cleanup(df):

    logger.info(
        "Limpeza final..."
    )

    df = df.dropna()

    return df


# SELECT FINAL COLUMNS

def select_final_columns(df):

    logger.info(
        "Selecionando colunas finais..."
    )

    final_columns = [

        "id",

        "id_data",

        "id_canal",

        "id_campanha",

        "id_regiao",

        "id_dispositivo",

        "id_audiencia",

        "impressoes",

        "clicks",

        "leads",

        "conversoes",

        "custo",

        "receita",

        "taxa_cliques",

        "taxa_conversao",

        "cpc",

        "roi",

        "criado_em"
    ]

    df = df[final_columns]

    return df

# MAIN TRANSFORM


def transform_data(df):

    try:

        logger.info(
            "Iniciando transformação..."
        )

        # ================================
        # STANDARDIZATION
        # ================================

        df = clean_channel_name(df)

        df = clean_device(df)

        # ================================
        # STRUCTURE
        # ================================

        df = split_campaign_info(df)

        # ================================
        # DATES
        # ================================

        df = clean_dates(df)

        # ================================
        # MONETARY
        # ================================

        df = clean_cost(df)

        df = clean_revenue(df)

        # ================================
        # NULLS
        # ================================

        df = handle_nulls(df)

        # ================================
        # VALID METRICS
        # ================================

        df = remove_invalid_metrics(df)

        # ================================
        # TYPES
        # ================================

        df = cast_types(df)

        # ================================
        # ID's
        # ================================
        
        df = add_dimension_ids(df)
        
        # ================================
        # DEDUP
        # ================================

        df = remove_duplicates(df)
        
        # ================================
        # METRICS
        # ================================
        
        df = create_metrics(df)

        # ================================
        # CLEANUP
        # ================================

        df = remove_infinite_values(df)

        df = final_cleanup(df)
        
        df = select_final_columns(df)

        logger.info(
            f"Transformação finalizada. "
            f"Total final: {len(df)} registros."
        )

        return df

    except Exception as e:

        logger.error(
            f"Erro na transformação: {e}",
            exc_info=True
        )

        raise