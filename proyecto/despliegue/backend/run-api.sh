podman run --replace -d --name fastapi \
    -v $(pwd):/app:Z \
    -w /app \
    -p 8000:8000 \
    python:3.10-slim \
    bash -c "
        pip install --no-cache-dir -r requirements.txt && \
        uvicorn main:app --host 0.0.0.0 --port 8000
    "
