# Dockerfile
FROM python:3.10

WORKDIR /app
COPY . .
RUN pip install --requirement requirements.txt && pip cache purge

ARG PORT
EXPOSE ${PORT:-8080}

CMD python -m streamlit run --server.port ${PORT:-8080} 🧭_Petunjuk.py