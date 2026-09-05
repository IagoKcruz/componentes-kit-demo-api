from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database.session import criar_tabelas, seed_tipos_usuario
from app.presentation.routers import usuario_router, servico_router, auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    seed_tipos_usuario()
    yield


app = FastAPI(
    title="Agendamentos API",
    description="API para sistema de agendamento de serviços",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(usuario_router.router)
app.include_router(servico_router.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "docs": "/docs"}
