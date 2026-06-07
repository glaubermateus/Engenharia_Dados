# LIBS
import pandas as pd
from faker import Faker
import random

def generate_dimensions():
    fake = Faker("pt_BR")

    # =========================================
    # DIM DATE
    # =========================================

    dates = pd.date_range(
        start="2025-01-01",
        end="2025-12-31"
    )

    dim_date = pd.DataFrame({
        "id_data": dates.strftime("%Y%m%d").astype(int),
        "data": dates,
        "ano": dates.year,
        "trimestre": dates.quarter,
        "mes": dates.month,
        "nome_mes": dates.strftime("%B"),
        "semana": dates.isocalendar().week,
        "dia": dates.day,
        "nome_dia": dates.day_name(),
        "fds": dates.weekday >= 5
    })

    nome_mes_pt = {
        "January" : "Janeiro",
        "February" : "Fevereiro",
        "March" : "Março",
        "April" : "Abril",
        "May" : "Maio",
        "June" : "Junho",
        "July" : "Julho",
        "August" : "Agosto",
        "September" : "Setembro",
        "October" : "Outubro",
        "November" : "Novembro",
        "December" : "Dezembro"
    }
    
    nome_dia_pt = {
        "Sunday" :  "Domingo",
        "Monday" :  "Segunda",
        "Tuesday" :  "Terça",
        "Wednesday" :  "Quarta",
        "Thursday" :  "Quinta",
        "Friday" :  "Sexta",
        "Saturday" :  "Sábado"
    }
    
    dim_date['nome_mes'] = dim_date['nome_mes'].map(nome_mes_pt)
    dim_date['nome_dia'] = dim_date['nome_dia'].map(nome_dia_pt)
    
    # DIM CHANNEL

    channels = [
        ("Google Ads", "Redes sociais pagas"),
        ("Meta Ads", "Redes sociais pagas"),
        ("LinkedIn Ads", "Redes sociais pagas"),
        ("TikTok Ads", "Redes sociais pagas"),
        ("Email Marketing", "CRM"),
        ("Busca orgânica", "Orgânico")
    ]

    dim_channel = pd.DataFrame(
        channels,
        columns=[
            "nome_canal",
            "tipo_canal"
        ]
    )

    dim_channel["id_canal"] = (
        dim_channel.index + 1
    )

    # DIM DEVICE

    devices = [
        "Celular",
        "Computador",
        "Tablet"
    ]

    dim_device = pd.DataFrame({
        "id_dispositivo": range(1, len(devices)+1),
        "tipo_dispositivo": devices
    })

    # DIM AUDIENCE

    audiences = []

    age_ranges = [
        "18-24",
        "25-34",
        "35-44",
        "45-54"
    ]

    genders = [
        "Masculino",
        "Feminino"
    ]

    income_levels = [
        "Baixo",
        "Medio",
        "Alto"
    ]

    audience_id = 1

    for age in age_ranges:
        for gender in genders:
            for income in income_levels:

                audiences.append({
                    "id_audiencia": audience_id,
                    "faixa_etaria": age,
                    "genero": gender,
                    "nivel_renda": income
                })

                audience_id += 1

    dim_audience = pd.DataFrame(audiences)

    # DIM REGION

    regions = []

    for i in range(20):

        regions.append({
            "id_regiao": i + 1,
            "pais": "Brasil",
            "estado": fake.state(),
            "cidade": fake.city()
        })

    dim_region = pd.DataFrame(regions)

    # DIM CAMPAIGN

    campaigns = []

    objectives = [
        "Conhecimento",
        "Tráfego",
        "Leads",
        "Conversão"
    ]

    statuses = [
        "Ativo",
        "Pausado",
        "Finalizado"
    ]

    campaign_types = [

    "Black Friday",

    "Natal",

    "Remarketing",

    "Conversão",

    "Geração de Leads",

    "Conhecimento",

    "Promoção",

    "Lançamento",

    "Retenção",

    "Carrinho Abandonado"
    ]

    products = [

        "Notebook",

        "Smartphone",

        "Curso",

        "Seguro",

        "Cartão",

        "Streaming",

        "Consultoria",

        "E-commerce"
        ]
    
    for i in range(50):

        campaigns.append({
            "id_campanha": i + 1,
            "nome_campanha": f"{random.choice(campaign_types)} - {random.choice(products)}",
            "objetivo": random.choice(objectives),
            "orcamento": round(random.uniform(5000, 50000), 2),
            "data_inicio": fake.date_between(
                start_date="-1y",
                end_date="today"
            ),
            "data_fim": fake.date_between(
                start_date="today",
                end_date="+6m"
            ),
            "status": random.choice(statuses)
        })

    dim_campaign = pd.DataFrame(campaigns)

    # LOAD TABLES

    tables = {
        "dim_data": dim_date,
        "dim_canal": dim_channel,
        "dim_dispositivo": dim_device,
        "dim_publico": dim_audience,
        "dim_regiao": dim_region,
        "dim_campanha": dim_campaign
    }

    return tables