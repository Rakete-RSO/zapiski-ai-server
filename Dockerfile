# Uporabi osnovno Python sliko
FROM python:3.12-slim

# Nastavi delovno mapo znotraj kontejnerja
WORKDIR /app

# Kopiraj datoteke v kontejner
COPY . /app

WORKDIR /app/frontend

RUN cp .example.env .env

# Namesti odvisnosti z `pip`
RUN pip install --no-cache-dir -r requirements.txt

# Razkritje vrat (8501 je privzeta vrata za Streamlit)
EXPOSE 8501

# Zagonski ukaz za aplikacijo
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]