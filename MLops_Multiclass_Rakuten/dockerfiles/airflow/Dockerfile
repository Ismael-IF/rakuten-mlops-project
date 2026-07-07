FROM apache/airflow:2.9.1

USER root
RUN apt-get update && apt-get install -y gosu
USER airflow

COPY requirements.txt requirements.txt

# Utilisation des contraintes
RUN pip install --no-cache-dir \
--constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.1/constraints-3.12.txt" \
-r requirements.txt
