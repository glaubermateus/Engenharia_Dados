# LIBS
import pandas as pd
from config.db import engine
from config.logger_config import logger
from utils.controle import get_last_processed_raw_id

# EXTRACT

def extract_raw_data():

    try:

        logger.info(
            "Extraindo dados RAW..."
        )

        last_raw_id = get_last_processed_raw_id()
        
        query = f"""
            SELECT *
            FROM raw.tb_raw_marketing
            WHERE id > {last_raw_id}
        """

        df = pd.read_sql(query, engine)

        logger.info(f"{len(df)} novos registros extraídos.")

        return df

    except Exception as e:

        logger.error(
            f"Erro na extracao: {e}",
            exc_info=True
        )

        raise