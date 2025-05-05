# backend/api.py (actualizado)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

app = FastAPI(title="Bodega API")

# Rutas de frontend
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

# Configurar CORS solo para desarrollo
if os.getenv("ENVIRONMENT", "development") == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# API Routes con prefijo
@app.get("/api/productos")
async def get_productos():
    # ... tu código API ...

# Servir frontend en producción
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")
    
    @app.get("/", include_in_schema=False)
    async def root():
        return FileResponse(FRONTEND_DIST / "index.html")
    
    @app.get("/{path:path}", include_in_schema=False)
    async def catch_all(path: str):
        if path.startswith("api/"):
            raise HTTPException(status_code=404)
        return FileResponse(FRONTEND_DIST / "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)