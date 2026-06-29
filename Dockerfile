# NOTE: .env must be present in rag-challenge/ before building.
# It is used during build to run scripts/index.py (requires VOYAGE_API_KEY).
# WARNING: secrets are baked into the image layer — do not push this image to a public registry.

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python scripts/index.py

VOLUME ["/app/chroma_db"]

EXPOSE 5000

CMD ["python", "run.py"]
