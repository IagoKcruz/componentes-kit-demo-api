from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dtos.auth_dto import LoginDTO, TokenResponseDTO
from app.application.use_cases.auth.login_use_case import LoginUseCase
from app.domain.exceptions.domain_exception import DomainException
from app.presentation.dependencies.dependencies import get_usuario_repository

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponseDTO)
async def login(dto: LoginDTO, repo=Depends(get_usuario_repository)):
    try:
        return await LoginUseCase(repo).executar(dto)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.mensagem)
