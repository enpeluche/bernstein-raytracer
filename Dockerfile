FROM pypy:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ pkg-config libfreetype6-dev libpng-dev libjpeg-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["pypy3", "main.py"]
