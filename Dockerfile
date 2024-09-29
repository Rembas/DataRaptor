FROM python:3.9-slim

# Installa le dipendenze necessarie
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    firefox-esr \
    --no-install-recommends

# Installa GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-linux64.tar.gz && \
    tar -xzf geckodriver-v0.32.2-linux64.tar.gz -C /usr/local/bin/ && \
    rm geckodriver-v0.32.2-linux64.tar.gz

WORKDIR /app
COPY . .

# Installa le dipendenze Python
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
