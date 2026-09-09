from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.infrastructure.database.session import criarTabelas
from app.infrastructure.database.seed import seedTiposUsuario
from app.presentation.routers import usuarioRouter, servicoRouter, authRouter
from app.domain.exceptions.entidadeNaoEncontradaError import EntidadeNaoEncontradaError
from app.domain.exceptions.validacaoError import ValidacaoError
from app.domain.exceptions.autenticacaoError import AutenticacaoError


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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(EntidadeNaoEncontradaError)
async def handleNaoEncontrado(_, exc: EntidadeNaoEncontradaError):
    return JSONResponse(status_code=404, content={"detail": exc.mensagem})


@app.exception_handler(ValidacaoError)
async def handleValidacao(_, exc: ValidacaoError):
    return JSONResponse(status_code=400, content={"detail": exc.mensagem})


@app.exception_handler(AutenticacaoError)
async def handleAutenticacao(_, exc: AutenticacaoError):
    return JSONResponse(status_code=401, content={"detail": exc.mensagem})


app.include_router(authRouter.router)
app.include_router(usuarioRouter.router)
app.include_router(servicoRouter.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "docs": "/docs"}
