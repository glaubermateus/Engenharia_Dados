# Pipeline de Previsão do Tempo com Apache Airflow

## 💡 Resumo do projeto

Esse projeto tem como objetivo desenvolver um pipeline automatizado em Apache Airflow para coletar dados meteorológicos de múltiplas cidades via API pública, transformar as informações relevantes e armazená-las em um banco SQLite para análises históricas e monitoramento climático.

## ❓ Problema de negócio / contexto

Organizações que dependem de dados climáticos (logística, energia, agronegócio, planejamento urbano, entre outras) precisam de informações atualizadas e estruturadas sobre o clima em diferentes regiões. A coleta manual ou esporádica desses dados dificulta análises históricas, comparações e automações.

Desse modo, este projeto resolve essa dor ao criar uma rotina automatizada e confiável que coleta, processa e armazena dados de previsão do tempo de forma recorrente, garantindo disponibilidade contínua das informações para análises e tomada de decisão.

## 📊 Dados utilizados

* Fonte dos dados: API pública do OpenWeatherMap
* Tipo de dados: Dados climáticos em (quase) tempo real
* Cidades monitoradas:
    * Indaiatuba, Blumenau, Palmas, Joinville, Santos, Curitiba, Fortaleza, Manaus, Betim e Juazeiro
* Principais atributos coletados:
    * Nome da cidade
    * Data da medição
    * Temperatura (em graus Celsius)
    * Descrição do clima (Ex.: céu limpo, nublado, chuva)
* Tratamentos aplicados:
    * Conversão de temperatura de Kelvin para Celsius
    * Padronização da data
    * Seleção apenas dos campos relevantes

## 🛠️ Metodologia e ferramentas

**Metodologia (ETL)**

1. Extração:
    * Consumo da API do OpenWeatherMap via requisições HTTP
    * Coleta dos dados brutos em formato JSON para cada cidade

2. Transformação:
    * Seleção das informações relevantes
    * Conversão de temperatura
    * Estruturação dos dados em formato tabular

3. Carga:
    * Criação automática da tabela e do banco SQLite, caso não exista
    * Ingestão dos dados na tabela

**Ferramentas e tecnologias**

* Apache Airflow: Orquestração e agendamento do pipeline
* Python: Linguagem principal do projeto
* SQLite: Banco de dados leve para armazenamento local
* Bibliotecas Python:
    * ```requests``` -> Consumo da API
    * ```sqlite3``` –> Interação com banco de dados
    * ```datetime``` –> Manipulação de datas
* Airflow Operators:
    * ```PythonOperator``` -> execução das funções de ETL

## 📈 Principais insights e resultados

* Criação de uma base histórica de dados climáticos por cidade
* Automação completa do processo, eliminando intervenção manual
* Estrutura pronta para:
    * Análises de variação de temperatura
    * Monitoramento climático por região
    * Integração futura com dashboards ou modelos analíticos
* Pipeline facilmente escalável para inclusão de novas cidades ou novos atributos climáticos

**Valor gerado**

Disponibilização contínua de dados confiáveis e estruturados, reduzindo esforço operacional e aumentando a capacidade analítica da organização.

## 🚀 Como executar o projeto

**Pré-requisitos**

* Docker e Docker Compose (recomendado para Airflow)
* Python 3.8+
* Apache Airflow configurado
* Acesso à API do OpenWeatherMap (chave de API válida)

**Pré-requisitos**

1. Clonar o repositório

```git clone https://github.com/glaubermateus/Engenharia_Dados.git```

```cd seu-repositorio```

2. Configurar o Airflow usando o Docker Desktop

* Instale o Docker Desktop

* Crie um diretório para seus arquivos do Airflow

* Navegue até ele

* Baixe o arquivo docker-compose.yaml da documentação oficial do Airflow (procure por "Docker Compose")

* Execute o comando para criar as imagens Docker do Airflow. Isso pode levar alguns minutos.

    ```docker compose up airflow-init```

* Execute o comando para inicializar o airflow

    ```docker compose up```

* Acesse o Airflow em http://localhost:8080. Use admin/admin como usuário/senha iniciais (ou as credenciais definidas no .env se usar a instalação padrão).

* Criar a seguinte estrutura de pastas:
    * config
    * dags
    * logs
    * plugins

* Coloque o arquivo Python da DAG dentro do diretório dags/ do Airflow
* Ajuste o caminho do banco SQLite, se necessário

3. Executar o projeto

* Acesse a interface web do Airflow
* Ative a DAG chamada projeto
* O pipeline será executado automaticamente conforme o agendamento (* * * * *, a cada minuto)

4. Visualizar os dados

* O banco **'banco_dados.db'** será criado automaticamente
* A tabela **'previsao_tempo'** conterá os dados processados

## 🤝 Contato

Glauber Cruz

[LinkedIn](https://www.linkedin.com/in/glauber-cruz-6213281b0/)

[Portfólio](https://sites.google.com/view/glaubercruz/p%C3%A1gina-inicial)
