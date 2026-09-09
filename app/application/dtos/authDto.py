from pydantic import BaseModel, EmailStr


class LoginDTO(BaseModel):
    email: EmailStr
    senha: str


class TokenResponseDTO(BaseModel):
    accessToken: str
    tokenType: str = "bearer"
