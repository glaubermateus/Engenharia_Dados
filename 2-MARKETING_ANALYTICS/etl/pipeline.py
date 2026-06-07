# LIBS
from config.logger_config import logger
from utils.controle import update_etl_control
from etl.extracao import extract_raw_data
from etl.transformacao import transform_data
from etl.validacao import validate_dataframe
from etl.carga import (load_staging, load_upsert)

# =========================================
# PIPELINE
# =========================================

def run_pipeline():

    try:
        logger.info(
            "=" * 60
        )
        
        logger.info(
            "PIPELINE INICIADA"
        )

        # EXTRACT
        df = extract_raw_data()
        
        # NO NEW DATA
        if df.empty:

                logger.info(
                    "Nenhum novo registro encontrado."
                )

                return
        
        # TRANSFORM
        df = transform_data(df)

        # VALIDATE
        df = validate_dataframe(df)

        # LOAD STAGING

        load_staging(df)

        # LOAD UPSERT

        load_upsert(df)

        logger.info(
            "PIPELINE FINALIZADA"
        )
    
    except Exception as e:
        logger.error(
            f"PIPELINE FALHOU: {e}",
            exc_info=True
        )

        logger.info(
            "=" * 60
        )

        raise

# MAIN

if __name__ == "__main__":
    run_pipeline()