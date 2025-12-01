# src/auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth import schema, service
from src.core.security import get_current_user
from src.db.session import get_db
from src.db.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])


# ============================
# REGISTER
# ============================
@router.post("/register", response_model=schema.UserResponse)
def register(
    data: schema.UserRegister,
    db: Session = Depends(get_db),
):
    try:
        user = service.register_user(db, data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ============================
# LOGIN (OAuth2 PASSWORD FLOW)
# ============================
@router.post("/login", response_model=schema.TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        token_data = service.login_user(
            db,
            email=form_data.username,   # Swagger envia o email como "username"
            password=form_data.password
        )
        return schema.TokenResponse(**token_data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ============================
# GET ME (TOKEN NECESSÁRIO)
# ============================
@router.get("/me", response_model=schema.UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user


# ============================
# ALTERAR SENHA (TOKEN OBRIGATÓRIO)
# ============================
@router.post("/alterar-senha")
def alterar_senha(
    data: schema.ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        service.change_password(
            db,
            user_id=current_user.id,
            senha_atual=data.senha_atual,
            nova_senha=data.nova_senha,
        )
        return {"mensagem": "Senha alterada com sucesso."}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ============================
# ESQUECI SENHA (SEM TOKEN)
# ============================
@router.post("/esqueci-senha")
def esqueci_senha(
    data: schema.ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    try:
        service.reset_password_by_email(
            db,
            email=data.email,
            nova_senha=data.nova_senha,
        )
        return {"mensagem": "Senha redefinida com sucesso."}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
