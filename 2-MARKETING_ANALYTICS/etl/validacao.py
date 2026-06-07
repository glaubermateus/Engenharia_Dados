# LIBS
import pandera as pa
from pandera import Check
from config.logger_config import logger

# SCHEMA

schema = pa.DataFrameSchema({

    "id": pa.Column(
        int,
        Check.ge(1),
        unique=True
    ),

    "id_data": pa.Column(
        int,
        Check.ge(1)
    ),

    "id_canal": pa.Column(
        int,
        Check.ge(1)
    ),

    "id_campanha": pa.Column(
        int,
        Check.ge(1)
    ),

    "id_regiao": pa.Column(
        int,
        Check.ge(1)
    ),

    "id_dispositivo": pa.Column(
        int,
        Check.ge(1)
    ),

    "id_audiencia": pa.Column(
        int,
        Check.ge(1)
    ),

    "impressoes": pa.Column(
        int,
        Check.ge(0)
    ),

    "clicks": pa.Column(
        int,
        Check.ge(0)
    ),

    "leads": pa.Column(
        int,
        Check.ge(0)
    ),

    "conversoes": pa.Column(
        int,
        Check.ge(0)
    ),

    "custo": pa.Column(
        float,
        Check.ge(0)
    ),

    "receita": pa.Column(
        float,
        Check.ge(0)
    ),

    "taxa_cliques": pa.Column(
        float,
        Check.in_range(0, 1)
    ),

    "taxa_conversao": pa.Column(
        float,
        Check.in_range(0, 1)
    ),

    "cpc": pa.Column(
        float,
        Check.ge(0)
    ),

    "roi": pa.Column(
        float,
        nullable=True
    ),

    "criado_em": pa.Column(
        pa.DateTime,
        nullable=False
    )
})

# VALIDATE

def validate_dataframe(df):

    try:

        logger.info(
            "Validando dataframe..."
        )

        validated_df = schema.validate(
            df,
            lazy=True
        )

        logger.info(
            "Validação concluída."
        )

        return validated_df

    except Exception as e:

        logger.error(
            f"Erro na validação: {e}",
            exc_info=True
        )

        raise