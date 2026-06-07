# LIBS
import random

# GENERATE METRICS

def generate_metrics():

    impressions = random.randint(
        1000,
        100000
    )

    ctr = random.uniform(
        0.01,
        0.08
    )

    clicks = int(
        impressions * ctr
    )

    # DIRTY DATA    

    if random.random() < 0.02:

        clicks = (
            impressions
            +
            random.randint(
                1,
                1000
            )
        )

    lead_rate = random.uniform(
        0.05,
        0.25
    )

    leads = int(
        clicks * lead_rate
    )

    conversion_rate = random.uniform(
        0.05,
        0.30
    )

    conversions = int(
        leads * conversion_rate
    )

    cpc = random.uniform(
        0.5,
        8
    )

    cost = round(
        clicks * cpc,
        2
    )

    ticket = random.uniform(
        100,
        1500
    )

    revenue = round(
        conversions * ticket,
        2
    )

    return {

        "impressoes":
        impressions,

        "clicks":
        clicks,

        "leads":
        leads,

        "conversoes":
        conversions,

        "custo":
        cost,

        "receita":
        revenue
    }