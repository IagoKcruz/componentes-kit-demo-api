# componentes-kit-demo-api

API REST do sistema de demonstração do [`componentes-kit`](https://github.com/IagoKcruz/componentes-kit). Fornece autenticação JWT e CRUD de Usuários e Serviços para o [frontend demo](https://github.com/IagoKcruz/componentes-kit-demo).

**Deploy:** https://componentes-kit-demo-api.onrender.com  
**Docs:** https://componentes-kit-demo-api.onrender.com/docs

## Stack

| Camada | Tecnologia |
|---|---|
| Framework | FastAPI + Python 3.12 |
| ORM | SQLModel (asyncpg) |
| Banco | PostgreSQL (Neon) |
| Auth | JWT via `python-jose` + bcrypt |
| Testes | pytest + pytest-asyncio |
| Deploy | Render |

## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha os valores:

```bash
cp .env.example .env
```

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | URL de conexão PostgreSQL com asyncpg (`postgresql+asyncpg://...`) |
| `JWT_SECRET` | Chave secreta para assinar os tokens (min. 16 chars) |
| `JWT_ALGORITMO` | Algoritmo JWT (padrão: `HS256`) |
| `JWT_EXPIRACAO_MINUTOS` | Tempo de vida do token (padrão: `60`) |
| `AUTH_HABILITADO` | `true` exige Bearer token nos endpoints protegidos |
| `CORS_ORIGINS` | Origens permitidas separadas por vírgula (ex: `https://componentes-kit-demo.vercel.app`) |
| `DEBUG` | `true` ativa logs SQL do SQLAlchemy |

## Rodando localmente

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
uvicorn main:app --reload
```

A API sobe em `http://localhost:8000`. As tabelas são criadas automaticamente no startup.

## Testes

```bash
pytest
```

## Estrutura

```
app/
├── domain/
│   ├── entities/        # Usuario, Servico (regras de negócio puras)
│   ├── value_objects/   # Email, CPF (com validação)
│   ├── enums/           # TipoUsuario
│   ├── exceptions/      # DomainException e subclasses
│   └── contracts/       # Interfaces de repositório e UoW
├── application/
│   ├── dtos/            # Schemas Pydantic de entrada/saída
│   ├── mappers/         # Conversão entidade ↔ DTO
│   └── use_cases/       # Casos de uso (criar, buscar, login…)
├── infrastructure/
│   ├── config.py        # Settings via Pydantic
│   ├── database/        # Engine, sessão, UoW, seed, models SQLModel
│   └── repositories/    # Implementações dos contratos de repositório
└── presentation/
    ├── routers/         # auth, usuario, servico
    └── dependencies/    # Injeção de dependências FastAPI
main.py                  # App FastAPI, middlewares, handlers de exceção
```

## Endpoints principais

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/auth/login` | Autentica e retorna JWT |
| `GET` | `/usuarios/` | Lista usuários |
| `POST` | `/usuarios/` | Cria usuário |
| `GET` | `/servicos/` | Lista serviços |
| `POST` | `/servicos/` | Cria serviço |
| `PATCH` | `/servicos/{id}` | Atualiza serviço |
| `DELETE` | `/servicos/{id}` | Remove serviço |

Documentação interativa completa em `/docs` (Swagger UI).
