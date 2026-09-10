from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.domain.exceptions.autenticacao_error import AutenticacaoError
from app.domain.exceptions.domain_exception import DomainException
from app.domain.exceptions.entidade_nao_encontrada_error import (
    EntidadeNaoEncontradaError,
)
from app.domain.exceptions.validacao_error import ValidacaoError
from app.infrastructure.config import settings
from app.infrastructure.database.seed import seedTiposUsuario
from app.infrastructure.database.session import criarTabelas
from app.presentation.routers import auth_router, servico_router, usuario_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await criarTabelas()
    await seedTiposUsuario()
    yield


app = FastAPI(
    title="Agendamentos API",
    description="API para sistema de agendamento de serviços",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_origin_regex=r"https://componentes-kit-demo-[^.]+\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def handleValidacaoPydantic(_: Request, exc: RequestValidationError):
    mensagens = [e["msg"].removeprefix("Value error, ") for e in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": "; ".join(mensagens)})


@app.exception_handler(DomainException)
async def handleDomainException(_, exc: DomainException):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(EntidadeNaoEncontradaError)
async def handleNaoEncontrado(_, exc: EntidadeNaoEncontradaError):
    return JSONResponse(status_code=404, content={"detail": exc.mensagem})


@app.exception_handler(ValidacaoError)
async def handleValidacao(_, exc: ValidacaoError):
    return JSONResponse(status_code=400, content={"detail": exc.mensagem})


@app.exception_handler(AutenticacaoError)
async def handleAutenticacao(_, exc: AutenticacaoError):
    return JSONResponse(status_code=401, content={"detail": exc.mensagem})


app.include_router(auth_router.router)
app.include_router(usuario_router.router)
app.include_router(servico_router.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "docs": "/docs"}
