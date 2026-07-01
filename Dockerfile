# Indexing runs at container startup, not at build time: the source document
# is a single page, so re-embedding it on every start is negligible (~seconds,
# one small Voyage API call) and keeps the index always in sync with the
# document baked into the image. It also means .env is never needed during
# build, so secrets aren't baked into any image layer.

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["sh", "-c", "python -m scripts.index && python run.py"]
