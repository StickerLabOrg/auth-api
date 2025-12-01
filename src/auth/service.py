# src/auth/service.py
from sqlalchemy.orm import Session

from src.auth import schema
from src.auth.repository import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    update_user_password,
)
from src.core.security import create_access_token, hash_password, verify_password
from src.db.models import User


def register_user(db: Session, data: schema.UserRegister) -> User:
    if get_user_by_email(db, data.email):
        raise ValueError("Email já registrado.")

    user = User(
        nome=data.nome,
        email=data.email,
        time_do_coracao=data.time_do_coracao,
        password_hash=hash_password(data.password),
    )
    return create_user(db, user)


# ============================================
# LOGIN — compatível com OAuth2PasswordRequestForm
# ============================================
def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Usuário não encontrado")

    if not verify_password(password, user.password_hash):
        raise ValueError("Senha incorreta")

    token = create_access_token({"sub": user.id})

    return {"access_token": token}


def change_password(
    db: Session,
    user_id: int,
    senha_atual: str,
    nova_senha: str,
) -> None:
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("Usuário não encontrado.")

    if not verify_password(senha_atual, user.password_hash):
        raise ValueError("Senha atual incorreta.")

    new_hash = hash_password(nova_senha)
    update_user_password(db, user, new_hash)


def reset_password_by_email(
    db: Session,
    email: str,
    nova_senha: str,
) -> None:
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Usuário não encontrado.")

    new_hash = hash_password(nova_senha)
    update_user_password(db, user, new_hash)
