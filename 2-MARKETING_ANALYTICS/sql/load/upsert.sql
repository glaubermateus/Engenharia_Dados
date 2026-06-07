INSERT INTO analytics.tb_analytics_marketing (

    id,
    id_data,
    id_canal,
    id_campanha,
    id_regiao,
    id_dispositivo,
    id_audiencia,
    impressoes,
    clicks,
    leads,
    conversoes,
    custo,
    receita,
    taxa_cliques,
    taxa_conversao,
    cpc,
    roi,
    criado_em

)

SELECT

    id,
    id_data,
    id_canal,
    id_campanha,
    id_regiao,
    id_dispositivo,
    id_audiencia,
    impressoes,
    clicks,
    leads,
    conversoes,
    custo,
    receita,
    taxa_cliques,
    taxa_conversao,
    cpc,
    roi,
    criado_em

FROM staging.tb_staging_marketing

ON CONFLICT (id)

DO UPDATE SET

    id_data = EXCLUDED.id_data,
    id_canal = EXCLUDED.id_canal,
    id_campanha = EXCLUDED.id_campanha,
    id_regiao = EXCLUDED.id_regiao,
    id_audiencia = EXCLUDED.id_audiencia,
    impressoes = EXCLUDED.impressoes,
    clicks = EXCLUDED.clicks,
    leads = EXCLUDED.leads,
    conversoes = EXCLUDED.conversoes,
    custo = EXCLUDED.custo,
    receita = EXCLUDED.receita,
    taxa_cliques = EXCLUDED.taxa_cliques,
    taxa_conversao = EXCLUDED.taxa_conversao,
    cpc = EXCLUDED.cpc,
    roi = EXCLUDED.roi,
    criado_em = EXCLUDED.criado_em