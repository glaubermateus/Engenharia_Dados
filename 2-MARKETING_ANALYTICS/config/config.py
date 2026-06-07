# LIBS
from pathlib import Path
import os

# VARS
raiz = Path(__file__).resolve().parent.parent

env_path = os.path.join(raiz, "config\\.env")

dados_dimensao = os.path.join(raiz, "dados\\dimensao")
os.makedirs(dados_dimensao, exist_ok=True)

dados_fato = os.path.join(raiz, "dados\\fato")
os.makedirs(dados_fato, exist_ok=True)