from fastapi import FastAPI, Request, HTTPException
from app1.routes import router as app1_router

app = FastAPI()

# Relación exacta entre dominio y ruta
DOMAIN_APP_MAP = {
    "rootfiles.me": "/app1",
    "lucasvilla.com": "/app2"
}

@app.middleware("http")
async def host_path_strict_checker(request: Request, call_next):
    host = request.headers.get("host", "").split(":")[0]
    path = request.url.path

    if host not in DOMAIN_APP_MAP:
        raise HTTPException(status_code=403, detail="Dominio no autorizado")

    expected_prefix = DOMAIN_APP_MAP[host]
    
    # Verifica que el path empiece EXACTAMENTE por su ruta asociada
    if not path.startswith(expected_prefix):
        raise HTTPException(status_code=403, detail="Ruta no permitida para este dominio")

    return await call_next(request)

# Incluir solo si pasa el middleware
app.include_router(app1_router, prefix="/app1")

