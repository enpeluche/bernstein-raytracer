FROM pypy:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ pkg-config libfreetype6-dev libpng-dev libjpeg-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*

RUN useradd -u 1000 -m appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

CMD ["pypy3", "src/main.py"]
