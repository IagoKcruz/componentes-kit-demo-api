from fastapi import APIRouter, Depends

from app.application.dtos.auth_dto import LoginDTO, TokenResponseDTO
from app.application.use_cases.auth.login_use_case import LoginUseCase
from app.presentation.dependencies.dependencies import getLoginUseCase

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponseDTO)
async def login(dto: LoginDTO, useCase: LoginUseCase = Depends(getLoginUseCase)):
    return await useCase.executar(dto)
