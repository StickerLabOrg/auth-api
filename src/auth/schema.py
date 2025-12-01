# src/auth/schema.py
from pydantic import BaseModel, EmailStr, field_validator


# ============================
# REGISTER
# ============================
class UserRegister(BaseModel):
    nome: str
    email: EmailStr
    password: str
    time_do_coracao: str | None = None

    @field_validator("password")
    def validar_senha(cls, v):
        if len(v) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")
        return v


# ============================
# USER RESPONSE
# ============================
class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    time_do_coracao: str | None = None

    model_config = {"from_attributes": True}  # Pydantic v2


# ============================
# LOGIN (não usado no Swagger)
# ============================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ============================
# TOKEN RESPONSE
# ============================
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============================
# CHANGE PASSWORD
# ============================
class ChangePasswordRequest(BaseModel):
    senha_atual: str
    nova_senha: str

    @field_validator("nova_senha")
    def validar_nova_senha(cls, v):
        if len(v) < 4:
            raise ValueError("A nova senha deve ter pelo menos 4 caracteres.")
        return v


# ============================
# FORGOT PASSWORD
# ============================
class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    nova_senha: str

    @field_validator("nova_senha")
    def validar_nova_senha(cls, v):
        if len(v) < 4:
            raise ValueError("A nova senha deve ter pelo menos 4 caracteres.")
        return v
