from fastapi import APIRouter, Depends
from app.application.dtos.authDto import LoginDTO, TokenResponseDTO
from app.application.useCases.auth.loginUseCase import LoginUseCase
from app.presentation.dependencies.dependencies import getLoginUseCase

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponseDTO)
async def login(dto: LoginDTO, useCase: LoginUseCase = Depends(getLoginUseCase)):
    return await useCase.executar(dto)
