from fastapi import APIRouter, Depends
from app.application.dtos.auth_dto import LoginDTO, TokenResponseDTO
from app.application.use_cases.auth.login_use_case import LoginUseCase
from app.presentation.dependencies.dependencies import get_usuario_repository

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponseDTO)
async def login(dto: LoginDTO, repo=Depends(get_usuario_repository)):
    return await LoginUseCase(repo).executar(dto)
