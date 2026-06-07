-- SCHEMAS

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS dimensions;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS control;

-- DIM_DATA

CREATE TABLE IF NOT EXISTS dimensions.dim_data (

    id_data            BIGINT PRIMARY KEY,

    data               DATE NOT NULL,

    ano                INT NOT NULL,

    trimestre          INT NOT NULL,

    mes                INT NOT NULL,

    nome_mes           VARCHAR(20) NOT NULL,

    semana             INT NOT NULL,

    dia                INT NOT NULL,

    nome_dia           VARCHAR(20) NOT NULL,

    fds                BOOLEAN NOT NULL
);

-- DIM_CANAL

CREATE TABLE IF NOT EXISTS dimensions.dim_canal (

    id_canal           BIGSERIAL PRIMARY KEY,

    nome_canal         VARCHAR(100) NOT NULL,

    tipo_canal         VARCHAR(50) NOT NULL
);

-- DIM_DISPOSITIVO

CREATE TABLE IF NOT EXISTS dimensions.dim_dispositivo (

    id_dispositivo     BIGINT PRIMARY KEY,

    tipo_dispositivo   VARCHAR(50) NOT NULL
);

-- DIM_PUBLICO

CREATE TABLE IF NOT EXISTS dimensions.dim_publico (

    id_audiencia       BIGINT PRIMARY KEY,

    faixa_etaria       VARCHAR(20) NOT NULL,

    genero             VARCHAR(20) NOT NULL,

    nivel_renda        VARCHAR(20) NOT NULL
);

-- DIM_REGIAO

CREATE TABLE IF NOT EXISTS dimensions.dim_regiao (

    id_regiao          BIGINT PRIMARY KEY,

    pais               VARCHAR(100) NOT NULL,

    estado             VARCHAR(100) NOT NULL,

    cidade             VARCHAR(100) NOT NULL
);

-- DIM_CAMPANHA

CREATE TABLE IF NOT EXISTS dimensions.dim_campanha (

    id_campanha        BIGINT PRIMARY KEY,

    nome_campanha      VARCHAR(255) NOT NULL,

    objetivo           VARCHAR(100) NOT NULL,

    orcamento          NUMERIC(18,2),

    data_inicio        DATE,

    data_fim           DATE,

    status             VARCHAR(50)
);

-- RAW FACT TABLE

CREATE TABLE IF NOT EXISTS raw.tb_raw_marketing (

    id                  BIGINT PRIMARY KEY,

    data_evento         VARCHAR(50),

    nome_canal          VARCHAR(255),

    info_campanha       VARCHAR(500),

    id_regiao           BIGINT,

    tipo_dispositivo    VARCHAR(100),

    id_audiencia        BIGINT,

    impressoes          BIGINT,

    clicks              BIGINT,

    leads               BIGINT,

    conversoes          BIGINT,

    custo               VARCHAR(100),

    receita             VARCHAR(100),

    criado_em           TIMESTAMP
);

-- STAGING FACT TABLE

CREATE TABLE IF NOT EXISTS staging.tb_staging_marketing (

    id              BIGINT PRIMARY KEY,

    id_data             BIGINT,

    id_canal            BIGINT,

    id_campanha         BIGINT,

    id_regiao           BIGINT,

    id_dispositivo      BIGINT,

    id_audiencia        BIGINT,

    impressoes          BIGINT,

    clicks              BIGINT,

    leads               BIGINT,

    conversoes          BIGINT,

    custo               NUMERIC(18,2),

    receita             NUMERIC(18,2),

    ctr                 NUMERIC(18,6),

    taxa_conversao      NUMERIC(18,6),

    roi                NUMERIC(18,6),

    criado_em           TIMESTAMP
);

-- ANALYTICS FACT TABLE

CREATE TABLE IF NOT EXISTS analytics.tb_marketing_analytics (

    id              BIGINT PRIMARY KEY,

    id_data             BIGINT NOT NULL,

    id_canal            BIGINT NOT NULL,

    id_campanha         BIGINT NOT NULL,

    id_regiao           BIGINT NOT NULL,

    id_dispositivo      BIGINT NOT NULL,

    id_audiencia        BIGINT NOT NULL,

    impressoes          BIGINT,

    clicks              BIGINT,

    leads               BIGINT,

    conversoes          BIGINT,

    custo               NUMERIC(18,2),

    receita             NUMERIC(18,2),

    ctr                 NUMERIC(18,6),

    taxa_conversao      NUMERIC(18,6),

    roi                NUMERIC(18,6),

    criado_em           TIMESTAMP,

    -- FOREIGN KEYS

    CONSTRAINT fk_fact_data
        FOREIGN KEY (id_data)
        REFERENCES dimensions.dim_data(id_data),

    CONSTRAINT fk_fact_canal
        FOREIGN KEY (id_canal)
        REFERENCES dimensions.dim_canal(id_canal),

    CONSTRAINT fk_fact_campanha
        FOREIGN KEY (id_campanha)
        REFERENCES dimensions.dim_campanha(id_campanha),

    CONSTRAINT fk_fact_regiao
        FOREIGN KEY (id_regiao)
        REFERENCES dimensions.dim_regiao(id_regiao),

    CONSTRAINT fk_fact_dispositivo
        FOREIGN KEY (id_dispositivo)
        REFERENCES dimensions.dim_dispositivo(id_dispositivo),

    CONSTRAINT fk_fact_publico
        FOREIGN KEY (id_audiencia)
        REFERENCES dimensions.dim_publico(id_audiencia)
);

-- ETL CONTROL

CREATE TABLE IF NOT EXISTS control.etl_control (

    id_controle            BIGSERIAL PRIMARY KEY,

    pipeline               VARCHAR(100),

    id_ultimo_registro     BIGINT,

    ultima_execucao        TIMESTAMP,

    status                 VARCHAR(50)
);