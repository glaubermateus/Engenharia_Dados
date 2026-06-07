# LIBS
import pandas as pd
from config.db import engine
from config.logger_config import logger
from utils.carregar_sql import load_sql

# GET LAST RAW ID (GERADOR_TB_FATO_INCREMENTAL)

def get_max_raw_id():

    query = """
        SELECT COALESCE(MAX(id),0) AS max_id
        FROM raw.tb_raw_marketing
    """

    result = pd.read_sql(query, engine)

    return int(result["max_id"][0])

# GET LAST PROCESSED RAW ID (ETL CONTROL)

def get_last_processed_raw_id():

    try:

        logger.info(
            "Buscando último ID..."
        )

        # LOAD SQL

        query = load_sql("sql/control/get_last_raw_id.sql")

        # EXECUTE

        result = pd.read_sql(query,engine)

        last_raw_id = result["id_ultimo_registro"][0]

        logger.info(
            f"""
            Último ID encontrado:

            {last_raw_id}
            """
        )

        return last_raw_id

    except Exception as e:

        logger.error(
            f"""
            Erro ao buscar
            último ID:

            {e}
            """,
            exc_info=True
        )

        raise

# UPDATE ETL CONTROL

def update_etl_control(last_raw_id):

    try:

        logger.info(
            "Atualizando ETL control..."
        )

        # DF

        df = pd.DataFrame([{"pipeline" : "marketing_pipeline", 
            "id_ultimo_registro": last_raw_id,
            "ultima_execucao": pd.Timestamp.now(),
            "status": "SUCESSO"
        }])

        # LOADING
        
        df.to_sql("etl_control", engine, schema="control", if_exists="append", index=False)

        logger.info(
            f"""
            Controle ETL atualizado.

            Último ID:
            {last_raw_id}
            """
        )

    except Exception as e:

        logger.error(
            f"""
            Erro ao atualizar
            ETL control:

            {e}
            """,
            exc_info=True
        )

        raise