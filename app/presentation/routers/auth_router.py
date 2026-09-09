from fastapi import APIRouter, Depends
from app.application.dtos.auth_dto import LoginDTO, TokenResponseDTO
from app.application.use_cases.auth.login_use_case import LoginUseCase
from app.presentation.dependencies.dependencies import get_login_use_case

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponseDTO)
async def login(dto: LoginDTO, use_case: LoginUseCase = Depends(get_login_use_case)):
    return await use_case.executar(dto)
