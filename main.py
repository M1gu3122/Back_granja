from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user,tareas,reportes,graficos,galpones,lotes,huevos
import uvicorn


# Inicialización de la app FastAPI
app = FastAPI()
@app.get("/")
def root():
    return {"message": "Bienvenido al backend FastAPI"}

app.include_router(user.router)
app.include_router(tareas.router)
app.include_router(reportes.router)
app.include_router(graficos.router)
app.include_router(galpones.router)
app.include_router(lotes.router)
app.include_router(huevos.router)

# Configurar CORS para permitir el acceso desde dominios externos
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Permitir todos los orígenes. Cambia a una lista específica de dominios si lo prefieres
    allow_credentials=True,
    allow_methods=[
        "*"
    ],  # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


# Comando para correr la aplicación usando Uvicornn
# if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=3000 )
