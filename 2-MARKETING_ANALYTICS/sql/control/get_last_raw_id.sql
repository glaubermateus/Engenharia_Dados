SELECT
    COALESCE(MAX(id_ultimo_registro), 0)
    AS id_ultimo_registro
FROM control.etl_control
WHERE pipeline = 'marketing_pipeline'