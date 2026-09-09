from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.infrastructure.database.session import criar_tabelas
from app.infrastructure.database.seed import seed_tipos_usuario
from app.presentation.routers import usuario_router, servico_router, auth_router
from app.domain.exceptions.entidade_nao_encontrada_error import EntidadeNaoEncontradaError
from app.domain.exceptions.validacao_error import ValidacaoError
from app.domain.exceptions.autenticacao_error import AutenticacaoError


@asynccontextmanager
async def lifespan(app: FastAPI):
    await criar_tabelas()
    await seed_tipos_usuario()
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


@app.exception_handler(EntidadeNaoEncontradaError)
async def handle_nao_encontrado(_, exc: EntidadeNaoEncontradaError):
    return JSONResponse(status_code=404, content={"detail": exc.mensagem})


@app.exception_handler(ValidacaoError)
async def handle_validacao(_, exc: ValidacaoError):
    return JSONResponse(status_code=400, content={"detail": exc.mensagem})


@app.exception_handler(AutenticacaoError)
async def handle_autenticacao(_, exc: AutenticacaoError):
    return JSONResponse(status_code=401, content={"detail": exc.mensagem})


app.include_router(auth_router.router)
app.include_router(usuario_router.router)
app.include_router(servico_router.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "docs": "/docs"}
