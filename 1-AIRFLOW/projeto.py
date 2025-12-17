# Importações
import os
import requests
import sqlite3
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Airflow
default_args = {
    "owner":"Data Science Academy",
    "depends_on_past":False,
    "start_date":datetime(2024,5,3),
    "retries":1,
    "retry_delay":timedelta(minutes=1)
}

# Airflow
dag = DAG('projeto', default_args = default_args, schedule_interval = "* * * * *", catchup = False)

# Função para extrair os dados da API
# http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=5a4930f3cc87a81b68156de8e5365d1c
def extrai_dados():
    URL_BASE = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "5a4930f3cc87a81b68156de8e5365d1c"
    CIDADES = ["Indaiatuba", "Blumenau", "Palmas", "Joinville", "Santos", "Curitiba", "Fortaleza", "Manaus", "Betim", "Juazeiro"]
    dados_cidades = []
    for cidade in CIDADES:
        url = f"{URL_BASE}q={cidade}&appid={API_KEY}"
        response = requests.get(url).json()
        dados_cidades.append(response)
    return dados_cidades
   
 # Função para transformar os dados extraídos
def transforma_dados(dados_cidades):
    dados_transformados = []
    for cidade in dados_cidades:
        dados_tempo = {
            "city":cidade['name'],
            "date":datetime.utcfromtimestamp(cidade['dt']).strftime('%Y-%m-%d'),
            "temperature":round(cidade['main']['temp'] - 273.15, 2),
            "weather":cidade['weather'][0]['description']
        }
        dados_transformados.append(dados_tempo)
    return dados_transformados

# Função para carregar os dados transformados
def carrega_dados(dados_transformados):
    conn = sqlite3.connect('/opt/airflow/dags/banco_dados.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS previsao_tempo (id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, date TEXT, temperature REAL, weather TEXT)
        '''
    )
    for dados in dados_transformados:
        cursor.execute('''
        INSERT INTO previsao_tempo(city, date, temperature, weather)
        VALUES (?,?,?,?)
        ''', (dados['city'], dados['date'], dados['temperature'], dados['weather']))
    conn.commit()
    conn.close()
    
# Airflow
# Criação das tarefas
tarefa_extrai_dados = PythonOperator(task_id = 'extrai_dados', python_callable = extrai_dados, dag = dag)
tarefa_transforma_dados = PythonOperator(task_id = 'transforma_dados', python_callable = transforma_dados, op_args = [tarefa_extrai_dados.output], dag = dag)
tarefa_carrega_dados = PythonOperator(task_id = 'carrega_dados', python_callable = carrega_dados, op_args = [tarefa_transforma_dados.output], dag = dag)

# Airflow
# Define a sequência de execução das tarefas
tarefa_extrai_dados >> tarefa_transforma_dados >> tarefa_carrega_dados