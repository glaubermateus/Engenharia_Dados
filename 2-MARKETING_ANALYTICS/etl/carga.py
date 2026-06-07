# LIBS
from sqlalchemy import text
from config.db import engine
from config.logger_config import logger
from utils.carregar_sql import load_sql
from utils.controle import update_etl_control

# LOAD ANALYTICS UPSERT

def load_staging(df):
    
    try:

        logger.info(
            "Iniciando load staging..."
        )

        # LOAD STAGING
        
        df.to_sql("tb_staging_marketing", engine, schema="staging", if_exists="append", index=False)

        logger.info(
            f"""
            Staging carregada.

            Registros:
            {len(df)}
            """
        )
    
    except Exception as e:
        logger.error(
            f"""
            Erro no load staging:

            {e}
            """,
            exc_info=True
        )

        raise


# EXECUTE UPSERT

def load_upsert(df):

    try:
        
        logger.info(
            "Executando UPSERT..."
        )
        
        # LOAD UPSERT SQL
        
        query = load_sql("sql/load/upsert.sql")

        # EXECUTE

        with engine.begin() as conn:

            conn.execute(text(query))

        logger.info(
            f"""
            UPSERT concluído.

            Registros processados:
            {len(df)}
            """
        )

        # UPDATE ETL CONTROL

        last_raw_id = df["id"].max()
        
        update_etl_control(last_raw_id)
    
    except Exception as e:

        logger.error(
            f"""
            Erro no UPSERT:

            {e}
            """,
            exc_info=True
        )

        raise